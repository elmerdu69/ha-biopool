from __future__ import annotations

from homeassistant.components.switch import SwitchEntity

from .api import BioPoolDevice
from .const import (
    DEVICE_DEFINITIONS,
    DOMAIN,
)
from .entity import BioPoolDeviceEntity
import asyncio

async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    """Create BioPool switches."""

    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for function, definition in DEVICE_DEFINITIONS.items():

        if definition["switch"]:

            entities.append(
                BioPoolSwitch(
                    coordinator,
                    function,
                )
            )

    async_add_entities(entities)


class BioPoolSwitch(
    BioPoolDeviceEntity,
    SwitchEntity,
):
    """BioPool equipment switch."""

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
            f"{self.unique_prefix}_switch"
        )

    @property
    def name(self):

        return "Marche / Arrêt"

    @property
    def icon(self):

        return self.device.icon

    @property
    def is_on(self):

        return self.device.is_on


    async def async_turn_on(self):

        await self.api.set_device(
            self.device.function,
            True,
        )

        await asyncio.sleep(2)

        await self.coordinator.async_request_refresh()


    async def async_turn_off(self):

        await self.api.set_device(
            self.device.function,
            False,
        )

        await asyncio.sleep(2)

        await self.coordinator.async_request_refresh()