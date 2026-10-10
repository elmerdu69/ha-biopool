from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import EntityCategory
from .entity import BioPoolDeviceEntity

from .const import (
    DOMAIN,
    FUNCTION_REACTOR,
    FUNCTION_OXY,
    FUNCTION_BACTER,
    PARAM_FORCE_UV,
    PARAM_FORCE_OXY,
    PARAM_FORCE_BACTER,
)


BUTTONS = {
    FUNCTION_REACTOR: {
        "name": "Forcer lampe UV",
        "icon": "mdi:lightbulb-fluorescent-tube",
        "parameter": PARAM_FORCE_UV,
    },
    FUNCTION_OXY: {
        "name": "Forcer oxygène actif",
        "icon": "mdi:molecule",
        "parameter": PARAM_FORCE_OXY,
    },
    FUNCTION_BACTER: {
        "name": "Forcer Bio-Bacter",
        "icon": "mdi:flask",
        "parameter": PARAM_FORCE_BACTER,
    },
}


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    """Create BioPool buttons."""

    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        BioPoolForceButton(coordinator, function)
        for function in BUTTONS
    ]
    entities.extend(
        BioPoolContainerResetButton(coordinator, function)
        for function in (FUNCTION_OXY, FUNCTION_BACTER)
    )
    entities.append(BioPoolUVResetButton(coordinator, FUNCTION_REACTOR))
    async_add_entities(entities)


class BioPoolContainerResetButton(BioPoolDeviceEntity, ButtonEntity):
    """Record a replacement treatment container."""

    _attr_has_entity_name = True
    _attr_name = "Remettre à 100 %"
    _attr_icon = "mdi:restore"
    _attr_entity_category = EntityCategory.CONFIG

    @property
    def unique_id(self):
        return f"{self.unique_prefix}_reset_remaining"

    async def async_press(self):
        """Reset the remaining amount, then read the controller state."""
        await self.api.reset_container_remaining(self._function)
        await self.coordinator.async_request_refresh()


class BioPoolUVResetButton(BioPoolContainerResetButton):
    """Record a replacement UV lamp through the dedicated API."""

    async def async_press(self):
        """Reset UV lifetime, then read the controller state."""
        await self.api.reset_uv_remaining()
        await self.coordinator.async_request_refresh()


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
            BUTTONS[self.function]["parameter"],
            True,
        )
        await self.coordinator.async_request_refresh()

    @property
    def available(self):
        return (
            self.coordinator.last_update_success
            and self.coordinator.data.get_device(self.function) is not None
        )

    @property
    def device_info(self):
        """Attach entity to its BioPool device."""

        device = self.coordinator.data.get_device(
            self.function
        )

        return device.device_info if device is not None else None
