from __future__ import annotations

import logging

from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import BioPoolAPI
from .const import (
    DOMAIN,
    UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class BioPoolCoordinator(DataUpdateCoordinator[BioPoolAPI]):
    """Coordinateur BioPool."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: BioPoolAPI,
    ) -> None:

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=UPDATE_INTERVAL,
            ),
        )

        self.api = api

    async def _async_update_data(self) -> BioPoolAPI:
        """Récupère les dernières données."""

        try:
            return await self.api.get_data()

        except Exception as err:
            raise UpdateFailed(
                f"Communication error: {err}"
            ) from err