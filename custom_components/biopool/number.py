from __future__ import annotations

from homeassistant.components.number import (
    NumberEntity,
    NumberMode,
)

from .const import (
    DOMAIN,
    NUMBER_TEMP_OFFSET,
)

from .entity import BioPoolControllerEntity


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    """Create BioPool number entities."""

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            BioPoolNumber(
                coordinator,
                NUMBER_TEMP_OFFSET,
            ),
        ]
    )


class BioPoolNumber(
    BioPoolControllerEntity,
    NumberEntity,
):
    """Controller number entity."""

    def __init__(
        self,
        coordinator,
        number_type,
    ):

        super().__init__(
            coordinator,
        )

        self.number_type = number_type

        self._attr_has_entity_name = True

        self._attr_mode = NumberMode.BOX

    @property
    def unique_id(self):

        return self.number_type

    @property
    def name(self):

        return "Décalage température"

    @property
    def native_min_value(self):

        return -10

    @property
    def native_max_value(self):

        return 10

    @property
    def native_step(self):

        return 0.1

    @property
    def native_unit_of_measurement(self):

        return "°C"

    @property
    def native_value(self):

        return self.api.temp_offset

    async def async_set_native_value(
        self,
        value: float,
    ):

        await self.api.set_temp_offset(
            round(value, 1),
        )

        await self.coordinator.async_request_refresh()