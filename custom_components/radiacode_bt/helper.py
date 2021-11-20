"""Helper functions"""
import typing

from bluepy.btle import DefaultDelegate
from bluepy.btle import Scanner


def discover_devices() -> typing.List[str]:
    """Performs BT scan for RadiaCode-101 devices"""

    class ScanDelegate(DefaultDelegate):
        def __init__(self):
            super().__init__()

    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(12.0)

    def is_radiocode(d) -> bool:
        return any("RadiaCode" in value for adtype, desc, value in d.getScanData())

    return [d.addr for d in devices if is_radiocode(d)]
