from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
)
from homeassistant.data_entry_flow import FlowResult

from .api import BioPoolAPI
from .const import DOMAIN


class BioPoolConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a BioPool config flow."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input=None,
    ) -> FlowResult:

        errors = {}

        if user_input is not None:

            api = BioPoolAPI(
                self.hass,
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD],
            )

            try:

                await api.login()

            except Exception:

                errors["base"] = "cannot_connect"

            else:

                await self.async_set_unique_id(
                    api._equipment_id
                )

                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title="BioPool",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {

                    vol.Required(
                        CONF_USERNAME,
                    ): str,

                    vol.Required(
                        CONF_PASSWORD,
                    ): str,

                }
            ),
            errors=errors,
        )