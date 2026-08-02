from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)

from .api import BioPoolDevice
from .const import (
    DEVICE_DEFINITIONS,
    DOMAIN,
)
from .entity import BioPoolDeviceEntity


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    """Create BioPool binary sensors."""

    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for function, definition in DEVICE_DEFINITIONS.items():

        if definition["binary_sensor"]:

            entities.append(
                BioPoolBinarySensor(
                    coordinator,
                    function,
                )
            )

    async_add_entities(entities)


class BioPoolBinarySensor(
    BioPoolDeviceEntity,
    BinarySensorEntity,
):
    """BioPool running state."""

    _attr_device_class = (
        BinarySensorDeviceClass.RUNNING
    )

    def __init__(
        self,
        coordinator,
        function: str,
    ):

        super().__init__(
            coordinator,
            function,
        )

        self._attr_has_entity_name = True

    @property
    def device(self) -> BioPoolDevice:
        return super().device

    @property
    def unique_id(self):

        return (
            f"{self.unique_prefix}_running"
        )

    @property
    def name(self):

        return "En fonctionnement"

    @property
    def icon(self):

        return self.device.icon

    @property
    def is_on(self):

        return self.device.is_running