"""
HID device helper for BLE.

Load ble hid device sequence object, then create Device class with the devices specified by report_ids,
Resemble the usb_hid.Device class interface.
"""

try:
    from typing import Sequence
except ImportError:
    pass


class Device:
    def __init__(
        self,
        devices: Sequence[object],
        report_ids: Sequence[int],
        # in_report_lengths: Sequence[int] = [], #no needed for now
        # out_report_lengths: Sequence[int] = [], #no needed for now
    ) -> None:
        # store as tuples to make them immutable-like and indexable
        self.devices = tuple(devices)
        self.report_ids = tuple(report_ids)
        # self.in_report_lengths = tuple(in_report_lengths)
        # self.out_report_lengths = tuple(out_report_lengths)

        # Precompute mappings from report_id to devices that can send reports
        # and to devices that expose a `report` attribute for reads.
        self._send_map = {rid: [] for rid in self.report_ids}
        self._report_map = {rid: [] for rid in self.report_ids}
        for dev in self.devices:
            dev_id = getattr(dev, "_report_id", None)
            if dev_id in self.report_ids:
                if hasattr(dev, "send_report"):
                    self._send_map.setdefault(dev_id, []).append(dev)
                if hasattr(dev, "report"):
                    self._report_map.setdefault(dev_id, []).append(dev)

    def _resolve_report_id(self, report_id):
        """Resolve effective report_id. If report_id is None and there's only
        one report id configured, use that one. Otherwise require explicit id.
        """
        if report_id is None:
            if len(self.report_ids) == 1:
                return self.report_ids[0]
            raise ValueError(
                "report_id must be provided when multiple report_ids exist")
        return report_id

    def send_report(self, report, report_id: int = None):
        """Send `report` to the first device in `devices` that matches the
        requested report_id and provides a `send_report` method.

        If multiple devices match, each matching device with a `send_report`
        method will receive the call (matching behavior mirrors the spec).
        """
        # Resolve effective report id
        target_id = self._resolve_report_id(report_id)

        # Directly iterate precomputed list for this report id
        for dev in self._send_map.get(target_id, ()):  # type: ignore[arg-type]
            dev.send_report(report)

        return None

    def get_last_received_report(self, report_id: int = None):
        """Return the last received OUT report (as bytes) for the first device
        that matches `report_id` and exposes a `report` attribute.

        If no matching device/report is found, returns None.
        """
        target_id = self._resolve_report_id(report_id)

        # Use precomputed list; return the first available report as bytes
        devs = self._report_map.get(target_id, ())
        if devs:
            return bytes(devs[0].report)

        return None
