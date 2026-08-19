from __future__ import annotations

from .const import (
    CONF_USE_EXTERNAL_TEMPERATURE,
    CONF_TEMPERATURE_ENTITY,
    CONF_BACTER_SIZE,
    CONF_OXY_SIZE,
    CONF_UV_LIFETIME,
    DEFAULT_BACTER_SIZE,
    DEFAULT_OXY_SIZE,
    DEFAULT_UV_LIFETIME,
)


class BioPoolSettings:
    """Runtime settings."""

    def __init__(
        self,
        options: dict,
    ):

        self.use_external_temperature = options.get(
            CONF_USE_EXTERNAL_TEMPERATURE,
            False,
        )

        self.temperature_entity = options.get(
            CONF_TEMPERATURE_ENTITY,
        )

        self.bacter_size = float(
            options.get(
                CONF_BACTER_SIZE,
                DEFAULT_BACTER_SIZE,
            )
        )

        self.oxy_size = float(
            options.get(
                CONF_OXY_SIZE,
                DEFAULT_OXY_SIZE,
            )
        )

        self.uv_lifetime = float(
            options.get(
                CONF_UV_LIFETIME,
                DEFAULT_UV_LIFETIME,
            )
        )