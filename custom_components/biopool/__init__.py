from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import BioPoolAPI
from .const import (
    DOMAIN,
    PLATFORMS,
)
from .coordinator import BioPoolCoordinator
from .settings import BioPoolSettings


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
        entry,
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

    entry.async_on_unload(entry.add_update_listener(async_update_options))

    return True


async def async_update_options(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Apply updated settings without discarding runtime counters."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    coordinator.api.settings = BioPoolSettings(entry.options)
    await coordinator.async_request_refresh()


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
