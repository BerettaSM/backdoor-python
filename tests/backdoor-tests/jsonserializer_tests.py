import pytest
from typing import Any

from backdoor.models.commands import Command
from backdoor.serialization.jsonserializer import JsonSerializer


@pytest.fixture
def serializer() -> JsonSerializer:
    return JsonSerializer()


class TestJsonSerializer:

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
        payload = Command("cmd", ["arg"], b"payload")

        result = serializer.serialize(payload)

        assert isinstance(result, bytes)

    def test_serialize_should_serialize_command_when_optional_fields_are_null(
        self, serializer: JsonSerializer
    ) -> None:
        payload = Command("cmd")

        result = serializer.serialize(payload)

        assert isinstance(result, bytes)

    def test_serialize_command_should_throw_when_payload_is_not_bytes(
        self, serializer: JsonSerializer
    ) -> None:
        payload = Command("cmd", ["arg"], "not bytes")  # type: ignore

        with pytest.raises(ValueError) as e:
            serializer.serialize(payload)

            assert e.match("Invalid payload type")

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

    def test_deserialize_command_should_throw_when_payload_is_not_str(
        self, serializer: JsonSerializer
    ) -> None:
        payload = '{"command":"cmd","args":null,"payload":0xCAFEBABE}'.encode()

        with pytest.raises(ValueError) as e:

            serializer.deserialize(payload)

            assert e.match("Invalid payload type")
