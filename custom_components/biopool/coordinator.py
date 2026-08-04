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
    CONF_USE_EXTERNAL_TEMPERATURE,
    CONF_TEMPERATURE_ENTITY,
)

_LOGGER = logging.getLogger(__name__)


class BioPoolCoordinator(DataUpdateCoordinator):
    """Coordinator for BioPool."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: BioPoolAPI,
        entry: ConfigEntry,
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
        self.config_entry = entry
        self._last_forced_temperature = object()

    async def _async_update_data(self):
        """Fetch data from BioPool."""

        try:

            options = self.config_entry.options

            use_external_temperature = options.get(
                CONF_USE_EXTERNAL_TEMPERATURE,
                False,
            )

            entity_id = options.get(
                CONF_TEMPERATURE_ENTITY,
            )

            if use_external_temperature and entity_id:

                state = self.hass.states.get(
                    entity_id
                )

                if (
                    state is not None
                    and state.state not in (
                        "unknown",
                        "unavailable",
                    )
                ):

                    try:

                        temperature = round(
                            float(state.state),
                            1,
                        )

                        #
                        # Envoie uniquement si la température change.
                        #
                        if (
                            temperature
                            != self._last_forced_temperature
                        ):

                            await self.api.set_forced_temperature(
                                temperature
                            )

                            self._last_forced_temperature = (
                                temperature
                            )

                    except (
                        TypeError,
                        ValueError,
                    ):

                        _LOGGER.warning(
                            "Invalid temperature value from %s: %s",
                            entity_id,
                            state.state,
                        )

            else:

                #
                # Retour au mode estimation.
                #
                if self._last_forced_temperature is not None:

                    await self.api.set_forced_temperature(
                        None
                    )

                    self._last_forced_temperature = None

            #
            # Lecture des données du contrôleur.
            #
            await self.api.get_data()

            return self.api

        except Exception as err:

            raise UpdateFailed(
                f"Communication error: {err}"
            ) from err