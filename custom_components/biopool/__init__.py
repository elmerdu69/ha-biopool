from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import BioPoolAPI
from .const import (
    DOMAIN,
    PLATFORMS,
)
from .coordinator import BioPoolCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up BioPool from a config entry."""

    api = BioPoolAPI(
        hass=hass,
        username=entry.data["username"],
        password=entry.data["password"],
        options=entry.options,
    )

    coordinator = BioPoolCoordinator(
        hass,
        api,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(
        DOMAIN,
        {}
    )[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:

        coordinator = hass.data[DOMAIN].pop(
            entry.entry_id
        )

        await coordinator.api.close()

    return unload_ok