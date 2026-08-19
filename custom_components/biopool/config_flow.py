from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import OptionsFlow
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
)
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .api import BioPoolAPI
from .const import (
    DOMAIN,
    CONF_USE_EXTERNAL_TEMPERATURE,
    CONF_TEMPERATURE_ENTITY,
    CONF_BACTER_SIZE,
    CONF_OXY_SIZE,
    CONF_UV_LIFETIME,
    DEFAULT_BACTER_SIZE,
    DEFAULT_OXY_SIZE,
    DEFAULT_UV_LIFETIME,
)


class BioPoolConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a BioPool config flow."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry):
        return BioPoolOptionsFlow(config_entry)

    async def async_step_user(
        self,
        user_input=None,
    ) -> FlowResult:

        errors = {}

        if user_input is not None:

            api = BioPoolAPI(
                hass=self.hass,
                username=user_input[CONF_USERNAME],
                password=user_input[CONF_PASSWORD],
                options={},
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


class BioPoolOptionsFlow(
    OptionsFlow,
):
    """BioPool options."""

    def __init__(
        self,
        config_entry,
    ):
        """Initialize options flow."""

        self._config_entry = config_entry

    @property
    def config_entry(self):
        """Return config entry."""

        return self._config_entry

    async def async_step_init(
        self,
        user_input=None,
    ):

        if user_input is not None:

            return self.async_create_entry(
                title="",
                data=user_input,
            )

        options = self.config_entry.options

        return self.async_show_form(

            step_id="init",

            data_schema=vol.Schema(

                {

                    vol.Optional(

                        CONF_USE_EXTERNAL_TEMPERATURE,

                        default=options.get(
                            CONF_USE_EXTERNAL_TEMPERATURE,
                            False,
                        ),

                    ): selector.BooleanSelector(),

                    vol.Optional(

                        CONF_TEMPERATURE_ENTITY,

                        default=options.get(
                            CONF_TEMPERATURE_ENTITY,
                            "",
                        ),

                    ): selector.EntitySelector(

                        selector.EntitySelectorConfig(
                            domain="sensor",
                            device_class="temperature",
                        )

                    ),

                    vol.Optional(

                        CONF_BACTER_SIZE,

                        default=options.get(
                            CONF_BACTER_SIZE,
                            DEFAULT_BACTER_SIZE,
                        ),

                    ): selector.NumberSelector(

                        selector.NumberSelectorConfig(
                            min=1,
                            max=100,
                            step=0.5,
                            unit_of_measurement="L",
                            mode=selector.NumberSelectorMode.BOX,
                        )

                    ),

                    vol.Optional(

                        CONF_OXY_SIZE,

                        default=options.get(
                            CONF_OXY_SIZE,
                            DEFAULT_OXY_SIZE,
                        ),

                    ): selector.NumberSelector(

                        selector.NumberSelectorConfig(
                            min=1,
                            max=100,
                            step=0.5,
                            unit_of_measurement="L",
                            mode=selector.NumberSelectorMode.BOX,
                        )

                    ),

                    vol.Optional(

                        CONF_UV_LIFETIME,

                        default=options.get(
                            CONF_UV_LIFETIME,
                            DEFAULT_UV_LIFETIME,
                        ),

                    ): selector.NumberSelector(

                        selector.NumberSelectorConfig(
                            min=1000,
                            max=20000,
                            step=100,
                            unit_of_measurement="h",
                            mode=selector.NumberSelectorMode.BOX,
                        )

                    ),

                }

            ),

        )