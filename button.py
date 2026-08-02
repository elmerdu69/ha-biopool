from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    MANUFACTURER,
    MODEL,
    FUNCTION_REACTOR,
    FUNCTION_OXY,
    FUNCTION_BACTER,
)


BUTTONS = {
    FUNCTION_REACTOR: {
        "name": "Forcer lampe UV",
        "icon": "mdi:lightbulb-on",
    },
    FUNCTION_OXY: {
        "name": "Forcer oxygène actif",
        "icon": "mdi:molecule",
    },
    FUNCTION_BACTER: {
        "name": "Forcer Bio-Bacter",
        "icon": "mdi:flask",
    },
}


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    """Create BioPool buttons."""

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        BioPoolForceButton(coordinator, function)
        for function in BUTTONS
    )


class BioPoolForceButton(
    CoordinatorEntity,
    ButtonEntity,
):
    """Force one treatment cycle."""

    def __init__(
        self,
        coordinator,
        function,
    ):
        super().__init__(coordinator)

        self.function = function

        definition = BUTTONS[function]

        self._attr_name = definition["name"]
        self._attr_icon = definition["icon"]

        self._attr_unique_id = (
            f"biopool_force_{function}"
        )

    async def async_press(self):
        """Force one treatment."""

        await self.coordinator.data.set_force(
            self.function,
            True,
        )

    @property
    def available(self):
        return self.coordinator.last_update_success

    @property
    def device_info(self):
        """Attach entity to its BioPool device."""

        device = self.coordinator.data.get_device(
            self.function
        )

        if device is None:
            identifier = self.function
            name = self._attr_name
        else:
            identifier = device.device_name
            name = device.name

        return {
            "identifiers": {
                (DOMAIN, identifier)
            },
            "name": name,
            "manufacturer": MANUFACTURER,
            "model": MODEL,
        }