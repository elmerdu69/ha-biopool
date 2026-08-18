from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from homeassistant.helpers.restore_state import RestoreEntity

from homeassistant.const import (
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTime,
    UnitOfTemperature,
    PERCENTAGE,
)

from .const import (
    DEVICE_DEFINITIONS,
    DOMAIN,
    CONF_BACTER_SIZE,
    CONF_OXY_SIZE,
    CONF_UV_LIFETIME,
    DEFAULT_BACTER_SIZE,
    DEFAULT_OXY_SIZE,
    DEFAULT_UV_LIFETIME,
    FUNCTION_REACTOR,
    FUNCTION_BACTER,
    FUNCTION_OXY,
)

from .entity import (
    BioPoolControllerEntity,
    BioPoolDeviceEntity,
)


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    """Create BioPool sensors."""

    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for function, definition in DEVICE_DEFINITIONS.items():

        if definition["power_sensor"]:
            entities.append(
                BioPoolSensor(
                    coordinator,
                    function,
                    "power",
                )
            )

        if definition["energy_sensor"]:
            entities.append(
                BioPoolSensor(
                    coordinator,
                    function,
                    "energy",
                )
            )

        if definition["runtime_sensor"]:
            entities.append(
                BioPoolSensor(
                    coordinator,
                    function,
                    "runtime",
                )
            )

        if definition["remaining_sensor"]:
            entities.append(
                BioPoolSensor(
                    coordinator,
                    function,
                    "remaining",
                )
            )

    entities.append(
        BioPoolControllerSensor(
            coordinator,
            "water_temp",
        )
    )

    async_add_entities(entities)


class BioPoolSensor(
    RestoreEntity,
    BioPoolDeviceEntity,
    SensorEntity,
):
    """BioPool sensor."""

    def __init__(
        self,
        coordinator,
        function: str,
        sensor_type: str,
    ):

        super().__init__(
            coordinator,
            function,
        )

        self.sensor_type = sensor_type

        self._attr_has_entity_name = True

        if sensor_type == "power":
            self._attr_suggested_display_precision = 0

        elif sensor_type == "energy":
            self._attr_suggested_display_precision = 2

        elif sensor_type == "runtime":
            self._attr_suggested_display_precision = 1

        elif sensor_type == "remaining":
            self._attr_suggested_display_precision = 1

    @property
    def unique_id(self):

        return (
            f"{self.device.unique_id}_{self.sensor_type}"
        )

    @property
    def name(self):

        if self.sensor_type == "power":
            return "Puissance"

        if self.sensor_type == "energy":
            return "Énergie"

        if self.sensor_type == "runtime":
            return "Temps de fonctionnement"

        if self.sensor_type == "remaining":

            if self.device.function == FUNCTION_REACTOR:
                return "Durée de vie restante"

            return "Quantité restante"

        return self.sensor_type

    @property
    def native_value(self):

        if self.sensor_type == "power":
            return self.device.power_w

        if self.sensor_type == "energy":
            return self.device.energy_kwh

        if self.sensor_type == "runtime":
            return self.device.runtime_h

        if self.sensor_type == "remaining":

            options = self.coordinator.config_entry.options

            if self.device.function == FUNCTION_REACTOR:
                maximum = options.get(CONF_UV_LIFETIME, DEFAULT_UV_LIFETIME)

            elif self.device.function == FUNCTION_BACTER:
                maximum = options.get(CONF_BACTER_SIZE, DEFAULT_BACTER_SIZE)

            elif self.device.function == FUNCTION_OXY:
                maximum = options.get(CONF_OXY_SIZE, DEFAULT_OXY_SIZE)

            else:
                return None

            if maximum <= 0:
                return None

            return round(
                max(
                    0,
                    self.device.consumed / maximum * 100,
                ),
                1,
            )

        return None
    
    @property
    def native_unit_of_measurement(self):

        if self.sensor_type == "power":
            return UnitOfPower.WATT

        if self.sensor_type == "energy":
            return UnitOfEnergy.KILO_WATT_HOUR

        if self.sensor_type == "runtime":
            return UnitOfTime.HOURS

        if self.sensor_type == "remaining":
            return PERCENTAGE

        return None

    @property
    def device_class(self):

        if self.sensor_type == "power":
            return SensorDeviceClass.POWER

        if self.sensor_type == "energy":
            return SensorDeviceClass.ENERGY

        if self.sensor_type == "runtime":
            return SensorDeviceClass.DURATION

        return None

    @property
    def state_class(self):

        if self.sensor_type == "power":
            return SensorStateClass.MEASUREMENT

        if self.sensor_type == "energy":
            return SensorStateClass.TOTAL_INCREASING

        if self.sensor_type == "runtime":
            return SensorStateClass.TOTAL_INCREASING

        return None

    @property
    def icon(self):

        if self.sensor_type == "power":
            return "mdi:flash"

        if self.sensor_type == "energy":
            return "mdi:lightning-bolt"

        if self.sensor_type == "runtime":
            return "mdi:timer-outline"

        if self.sensor_type == "remaining":

            if self.device.function == FUNCTION_REACTOR:
                return "mdi:lightbulb"

            return "mdi:cup-water"

        return self.device.icon

    @property
    def available(self):

        return (
            super().available
            and self.device is not None
        )

    async def async_added_to_hass(self):
        """Restore previous sensor state."""

        await super().async_added_to_hass()

        if self.sensor_type != "energy":
            return

        last_state = await self.async_get_last_state()

        if last_state is None:
            return

        try:

            restored_energy = float(
                last_state.state
            )

        except (
            TypeError,
            ValueError,
        ):

            return

        self.device.energy_kwh = restored_energy


class BioPoolControllerSensor(
    BioPoolControllerEntity,
    SensorEntity,
):
    """Global controller sensors."""

    def __init__(
        self,
        coordinator,
        sensor_type: str,
    ):

        super().__init__(
            coordinator,
        )

        self.sensor_type = sensor_type

        self._attr_has_entity_name = True

        self._attr_suggested_display_precision = 1

    @property
    def unique_id(self):

        return self.sensor_type

    @property
    def name(self):

        if self.sensor_type == "water_temp":
            return "Température de l'eau"

        return self.sensor_type

    @property
    def native_value(self):

        if self.sensor_type == "water_temp":
            return self.api.water_temp

        return None

    @property
    def native_unit_of_measurement(self):

        return UnitOfTemperature.CELSIUS

    @property
    def device_class(self):

        return SensorDeviceClass.TEMPERATURE

    @property
    def state_class(self):

        return SensorStateClass.MEASUREMENT

    @property
    def icon(self):

        return "mdi:coolant-temperature"