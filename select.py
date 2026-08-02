from __future__ import annotations

from homeassistant.components.select import SelectEntity

from .const import (
    DOMAIN,
    POOL_MODES,
    POOL_MODES_REVERSE,
)
from .entity import BioPoolControllerEntity


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    """Create BioPool mode selector."""

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            BioPoolModeSelect(
                coordinator,
            )
        ]
    )


class BioPoolModeSelect(
    BioPoolControllerEntity,
    SelectEntity,
):
    """Pool operating mode."""

    def __init__(
        self,
        coordinator,
    ):

        super().__init__(coordinator)

        self._attr_has_entity_name = True

        self._attr_name = "Mode de fonctionnement"

        self._attr_unique_id = "pool_mode"

        self._attr_icon = "mdi:cog"

        self._attr_options = list(
            POOL_MODES.values()
        )

    @property
    def current_option(self):

        if self.api.mode is None:
            return None

        return POOL_MODES.get(
            self.api.mode,
            self.api.mode,
        )

    async def async_select_option(
        self,
        option: str,
    ):

        await self.api.set_mode(
            POOL_MODES_REVERSE[option]
        )

        await self.coordinator.async_request_refresh()