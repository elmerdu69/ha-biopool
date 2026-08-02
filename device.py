from __future__ import annotations

from dataclasses import dataclass, field

from .const import (
    FUNCTION_BACTER,
    FUNCTION_OXY,
    FUNCTION_PUMP,
    FUNCTION_REACTOR,
)


@dataclass
class BioPoolDevice:
    """Represent one BioPool equipment."""

    function: str
    name: str

    power: str = "OFF"
    mode: str | None = None

    sensor_power: float = 0.0
    consumed: float | None = None

    force_uv: bool = False
    force_oxy: bool = False
    force_bacter: bool = False

    raw: dict = field(default_factory=dict)

    @property
    def is_on(self) -> bool:
        return self.power.upper() == "ON"

    @property
    def power_w(self) -> float:
        try:
            return float(self.sensor_power)
        except Exception:
            return 0.0

    @property
    def is_pump(self) -> bool:
        return self.function == FUNCTION_PUMP

    @property
    def is_reactor(self) -> bool:
        return self.function == FUNCTION_REACTOR

    @property
    def is_bacter(self) -> bool:
        return self.function == FUNCTION_BACTER

    @property
    def is_oxy(self) -> bool:
        return self.function == FUNCTION_OXY

    def update(self, data: dict) -> None:
        """Update device from API."""

        self.raw = data

        self.name = data.get("name", self.name)

        self.power = str(
            data.get("power", "OFF")
        ).upper()

        self.mode = data.get("mode")

        try:
            self.sensor_power = float(
                data.get("sensor-power", 0)
            )
        except Exception:
            self.sensor_power = 0.0

        try:
            self.consumed = float(
                data.get("consumed", 0)
            )
        except Exception:
            self.consumed = 0.0

        self.force_uv = bool(
            data.get("force_uv", False)
        )

        self.force_oxy = bool(
            data.get("force_oxy", False)
        )

        self.force_bacter = bool(
            data.get("force_bacter", False)
        )