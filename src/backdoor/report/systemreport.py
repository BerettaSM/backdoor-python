# pyright: reportUnusedVariable=false
import os
import platform
import socket
import time
from typing import LiteralString

import cpuinfo
import psutil
from psutil._common import snicaddr

from backdoor.models.systemreport import *


UNKNOWN = "unknown"


class SystemDataCollector:

    def __init__(self, report_expiry_in_seconds: int = 60) -> None:
        self.__timestamp = time.time()
        self.expiry = report_expiry_in_seconds
        self.report: SystemReport = self.__generate_report()

    def collect_data(self) -> SystemReport:
        if self.__should_refresh():
            self.__timestamp = time.time()
            self.refresh()
        return self.report

    def refresh(self) -> None:
        self.report = self.__generate_report()

    def __generate_report(self) -> SystemReport:
        identity = self.__system_identity()
        cpu_info = self.__cpu_info()
        mem_info = self.__mem_info()
        disk_info = self.__disk_info()
        network = self.__network_summary()
        hardware = HardwareSummary(**locals())
        return SystemReport(**locals())

    def __should_refresh(self) -> bool:
        return self.__timestamp + self.expiry <= time.time()

    def __system_identity(self) -> SystemIdentity:
        user = os.getlogin()
        hostname = socket.gethostname()
        _platform = platform.platform()
        boot_time = psutil.boot_time()
        return SystemIdentity(**locals(), platform=_platform)

    def __cpu_info(self) -> CpuInfo:
        cpu_info = cpuinfo.get_cpu_info()
        arch = cpu_info["arch"]
        brand = cpu_info["brand_raw"]
        version = cpu_info["cpuinfo_version_string"]
        frequency = cpu_info["hz_actual_friendly"]
        vendor_id = cpu_info["vendor_id_raw"]
        cores = cpu_info["count"]
        return CpuInfo(**locals())

    def __mem_info(self) -> MemInfo:
        mem = psutil.virtual_memory()
        total_bytes = mem.total
        total_str = f"{round(total_bytes / (1024**3), 2)} GB"
        return MemInfo(**locals())

    def __disk_info(self) -> list[DiskInfo]:
        disk_info: list[DiskInfo] = []
        disks = psutil.disk_partitions()
        for disk in disks:
            disk_usage = psutil.disk_usage(disk.device)
            disk_info.append(
                DiskInfo(
                    device=disk.device,
                    mountpoint=disk.mountpoint,
                    fstype=disk.fstype,
                    opts=disk.opts,
                    total_space=disk_usage.total,
                    free_space=disk_usage.free,
                )
            )
        return disk_info

    def __network_summary(self) -> NetworkSummary:
        net_ifs = psutil.net_if_addrs()
        interfaces = [
            self.__network_interface(name, snicaddrs)
            for name, snicaddrs in net_ifs.items()
        ]
        return NetworkSummary(interfaces=interfaces)

    def __network_interface(
        self, name: str, snicaddrs: list[snicaddr]
    ) -> NetworkInterfaceInfo:
        info: dict[LiteralString, str] = {}
        for addr in snicaddrs:
            match addr.family:
                case socket.AF_INET:
                    info["inet"] = addr.address or UNKNOWN
                    info["broadcast"] = addr.broadcast or UNKNOWN
                    info["netmask"] = addr.netmask or UNKNOWN
                case socket.AF_PACKET:
                    info["mac"] = addr.address or UNKNOWN
                case _:
                    ...
        return NetworkInterfaceInfo(name=name, **info)


if __name__ == "__main__":
    collector = SystemDataCollector()
    report = collector.collect_data()
    import pprint

    pprint.pprint(report)
