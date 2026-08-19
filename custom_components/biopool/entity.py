from __future__ import annotations

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import (
    DOMAIN,
    MANUFACTURER,
    MODEL,
)
from .coordinator import BioPoolCoordinator


class BioPoolEntity(CoordinatorEntity):
    """Base class for every BioPool entity."""

    def __init__(
        self,
        coordinator: BioPoolCoordinator,
    ):

        super().__init__(coordinator)

    @property
    def api(self):

        return self.coordinator.data

    @property
    def available(self):

        return self.coordinator.last_update_success


class BioPoolControllerEntity(
    BioPoolEntity,
):
    """Pool controller entity."""

    @property
    def device_info(self):

        return {

            "identifiers": {
                (
                    DOMAIN,
                    "pool",
                )
            },

            "name": "Piscine",

            "manufacturer": MANUFACTURER,

            "model": MODEL,

        }

    @property
    def api(self):
        return self.coordinator.api


class BioPoolDeviceEntity(
    BioPoolEntity,
):
    """Physical BioPool equipment."""

    def __init__(
        self,
        coordinator,
        function: str,
    ):

        super().__init__(
            coordinator,
        )

        self._function = function

    @property
    def device(self):

        return self.api.get_device(
            self._function
        )

    @property
    def available(self):

        return (

            super().available

            and

            self.device is not None

        )

    @property
    def unique_prefix(self):

        return self.device.unique_id

    @property
    def device_info(self):

        return self.device.device_info