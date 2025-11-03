import pytest
from typing import Any

from backdoor.models.commands import Command, CommandResult
from backdoor.models.systemreport import SystemReport
from backdoor.report.systemreport import SystemDataCollector
from backdoor.serialization.exceptions import BadDataError
from backdoor.serialization.jsonserializer import JsonSerializer


@pytest.fixture
def serializer() -> JsonSerializer:
    return JsonSerializer()


@pytest.fixture
def system_report() -> SystemReport:
    return SystemDataCollector().collect_data()


class TestJsonSerializer:

    def test_deserialize_bad_data_should_throw(
        self, serializer: JsonSerializer
    ) -> None:
        bad_data = "{alkdjfa,;lk1j23lkj312kl3j"

        with pytest.raises(BadDataError) as e:

            serializer.deserialize(bad_data.encode())

        assert e.match("unexpected format")

    def test_serialize_should_serialize_str(self, serializer: JsonSerializer) -> None:
        payload = "message"

        result = serializer.serialize(payload)

        assert f'"{payload}"'.encode() == result

    def test_deserialize_should_deserialize_str(
        self, serializer: JsonSerializer
    ) -> None:
        payload = b'"message"'

        result = serializer.deserialize(payload)

        assert "message" == result

    def test_serialize_should_serialize_int(self, serializer: JsonSerializer) -> None:
        payload = 42

        result = serializer.serialize(payload)

        assert str(payload).encode() == result

    def test_deserialize_should_deserialize_int(
        self, serializer: JsonSerializer
    ) -> None:
        payload = b"42"

        result = serializer.deserialize(payload)

        assert int(payload) == result

    def test_serialize_should_serialize_float(self, serializer: JsonSerializer) -> None:
        payload = 42.42

        result = serializer.serialize(payload)

        assert str(payload).encode() == result

    def test_deserialize_should_deserialize_float(
        self, serializer: JsonSerializer
    ) -> None:
        payload = b"42.42"

        result = serializer.deserialize(payload)

        assert float(payload) == result

    def test_serialize_should_serialize_none(self, serializer: JsonSerializer) -> None:
        payload = None

        result = serializer.serialize(payload)

        assert "null".encode() == result

    def test_deserialize_should_deserialize_none(
        self, serializer: JsonSerializer
    ) -> None:
        payload = b"null"

        result = serializer.deserialize(payload)

        assert result is None

    def test_serialize_should_serialize_bool_true(
        self, serializer: JsonSerializer
    ) -> None:
        payload = True

        result = serializer.serialize(payload)

        assert "true".encode() == result

    def test_deserialize_should_deserialize_bool_true(
        self, serializer: JsonSerializer
    ) -> None:
        payload = b"true"

        result = serializer.deserialize(payload)

        assert result

    def test_serialize_should_serialize_bool_false(
        self, serializer: JsonSerializer
    ) -> None:
        payload = False

        result = serializer.serialize(payload)

        assert "false".encode() == result

    def test_deserialize_should_deserialize_bool_false(
        self, serializer: JsonSerializer
    ) -> None:
        payload = b"false"

        result = serializer.deserialize(payload)

        assert not result

    def test_serialize_should_serialize_list(self, serializer: JsonSerializer) -> None:
        payload: list[Any] = ["hello", 42, True]

        result = serializer.serialize(payload)

        assert result.decode() == '["hello", 42, true]'

    def test_deserialize_should_deserialize_list(
        self, serializer: JsonSerializer
    ) -> None:
        payload = b'["hello", 42, true]'

        result = serializer.deserialize(payload)

        assert result == ["hello", 42, True]

    def test_serialize_should_serialize_dict(self, serializer: JsonSerializer) -> None:
        payload: dict[str, Any] = {
            "a": 1,
            "b": 42.69,
            "c": True,
            "d": False,
            "e": "hello",
            "f": None,
            "g": ["hello", 42, True],
        }

        result = serializer.serialize(payload)

        assert (
            result.decode()
            == '{"a": 1, "b": 42.69, "c": true, "d": false, "e": "hello", "f": null, "g": ["hello", 42, true]}'
        )

    def test_deserialize_should_deserialize_dict(
        self, serializer: JsonSerializer
    ) -> None:
        payload = b'{"a": 1, "b": 42.69, "c": true, "d": false, "e": "hello", "f": null, "g": ["hello", 42, true]}'

        result = serializer.deserialize(payload)

        assert isinstance(result, dict)

        for key in "a", "b", "c", "d", "e", "f", "g":
            assert key in result

    def test_serialize_should_serialize_command(
        self, serializer: JsonSerializer
    ) -> None:
        payload = Command(command="cmd", args=["arg"], payload=b"payload")

        result = serializer.serialize(payload)

        assert isinstance(result, bytes)

    def test_serialize_should_serialize_command_when_optional_fields_are_null(
        self, serializer: JsonSerializer
    ) -> None:
        payload = Command(command="cmd")

        result = serializer.serialize(payload)

        assert isinstance(result, bytes)

    def test_deserialize_should_deserialize_command(
        self, serializer: JsonSerializer
    ) -> None:
        payload = '{"command":"cmd","args":["arg"],"payload":"payload"}'.encode()

        result = serializer.deserialize(payload)

        assert isinstance(result, Command)

    def test_deserialize_should_deserialize_command_when_optional_fields_are_null(
        self, serializer: JsonSerializer
    ) -> None:
        payload = '{"command":"cmd","args":null,"payload":null}'.encode()

        result = serializer.deserialize(payload)

        assert isinstance(result, Command)
        assert result.args is None
        assert result.payload is None

    def test_serialize_should_serialize_command_result(
        self, serializer: JsonSerializer
    ) -> None:
        payload = CommandResult(
            success=True,
            returncode=0,
            stdout="stdout",
            stderr="stderr",
            payload=b"payload",
        )

        result = serializer.serialize(payload)

        assert isinstance(result, bytes)

    def test_serialize_should_serialize_command_result_when_optional_fields_are_null(
        self, serializer: JsonSerializer
    ) -> None:
        payload = CommandResult(success=True, returncode=0)

        result = serializer.serialize(payload)

        assert isinstance(result, bytes)

    def test_deserialize_should_deserialize_command_result(
        self, serializer: JsonSerializer
    ) -> None:
        payload = """
        {
            "success":true,
            "returncode":0,
            "stdout":"stdout",
            "stderr":"stderr",
            "payload":"payload"
        }
        """.encode()

        result = serializer.deserialize(payload)

        assert isinstance(result, CommandResult)

    def test_deserialize_should_deserialize_command_result_when_optional_fields_are_null(
        self, serializer: JsonSerializer
    ) -> None:
        payload = """
        {
            "success":true,
            "returncode":0
        }
        """.encode()

        result = serializer.deserialize(payload)

        assert isinstance(result, CommandResult)

    def test_serialize_should_serialize_system_report(
        self, serializer: JsonSerializer, system_report: SystemReport
    ) -> None:

        result = serializer.serialize(system_report)

        assert isinstance(result, bytes)

    def test_deserialize_should_deserialize_system_report(
        self, serializer: JsonSerializer, system_report: SystemReport
    ) -> None:
        payload = """
        {
            "identity": {
                "user": "user",
                "hostname": "host",
                "platform": "platform",
                "boot_time": 8.0
            },
            "hardware": {
                "cpu_info": {
                    "arch": "arch",
                    "brand": "brand",
                    "version": "1.0.0",
                    "frequency": "4.4501 GHz",
                    "vendor_id": "vendor_id",
                    "cores": 42
                },
                "mem_info": {
                    "total_bytes": 33569787904,
                    "total_str": "31.26 GB"
                },
                "disk_info": [
                    {
                        "device": "/dev/nvme0n1p1",
                        "mountpoint": "/boot",
                        "fstype": "vfat",
                        "opts": "rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=ascii,shortname=mixed,utf8,errors=remount-ro",
                        "total_space": 16757178368,
                        "free_space": 16757178368
                    }
                ]
            },
            "network": {
                "interfaces": [
                    {
                        "name": "lo",
                        "inet": "127.0.0.1",
                        "netmask": "255.0.0.0",
                        "broadcast": "unknown",
                        "mac": "00:00:00:00:00:00"
                    },
                    {
                        "name": "enp34s0",
                        "inet": "10.1.1.104",
                        "netmask": "255.255.255.0",
                        "broadcast": "10.1.1.255",
                        "mac": "11:22:33:44:55:66"
                    }
                ]
            }
        }
        """.encode()

        result = serializer.deserialize(payload)

        assert isinstance(result, SystemReport)
