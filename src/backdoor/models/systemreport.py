from pydantic import BaseModel


class SystemIdentity(BaseModel):
    user: str
    hostname: str
    platform: str
    boot_time: float


class CpuInfo(BaseModel):
    arch: str
    brand: str
    version: str
    frequency: str
    vendor_id: str
    cores: int


class MemInfo(BaseModel):
    total_bytes: int
    total_str: str


class DiskInfo(BaseModel):
    device: str
    mountpoint: str
    fstype: str
    opts: str
    total_space: int
    free_space: int


class HardwareSummary(BaseModel):
    cpu_info: CpuInfo
    mem_info: MemInfo
    disk_info: list[DiskInfo]


class NetworkInterfaceInfo(BaseModel):
    name: str
    inet: str
    netmask: str
    broadcast: str
    mac: str


class NetworkSummary(BaseModel):
    interfaces: list[NetworkInterfaceInfo]


class SystemReport(BaseModel):
    identity: SystemIdentity
    hardware: HardwareSummary
    network: NetworkSummary
