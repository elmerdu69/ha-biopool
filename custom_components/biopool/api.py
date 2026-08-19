from __future__ import annotations

import json
import logging
import time

from dataclasses import dataclass

from aiohttp import ClientSession

from homeassistant.helpers.aiohttp_client import (
    async_get_clientsession,
)

from .settings import BioPoolSettings

from .const import (
    BASE_URL,
    CMD_POWER,
    DEVICE_DEFINITIONS,
    FUNCTION_BACTER,
    FUNCTION_OXY,
    FUNCTION_PUMP,
    FUNCTION_REACTOR,
    PARAM_BACTER_SIZE,
    PARAM_FORCE_BACTER,
    PARAM_FORCE_OXY,
    PARAM_FORCE_UV,
    PARAM_MODE,
    PARAM_OXY_SIZE,
    POOL_MODES,
    PARAM_FORCE_TEMP,
)

_LOGGER = logging.getLogger(__name__)

@dataclass
class BioPoolDevice:
    """One physical BioPool equipment."""

    api: "BioPoolAPI"

    function: str

    device_name: str

    power: bool = False

    power_w: float = 0.0

    energy_kwh: float = 0.0

    runtime_h: float = 0.0

    mode: str | None = None

    force: bool = False

    @property
    def definition(self):
        return DEVICE_DEFINITIONS[self.function]

    @property
    def name(self):
        return self.definition["name"]

    @property
    def icon(self):
        return self.definition["icon"]

    @property
    def unique_id(self):
        return self.function

    @property
    def device_info(self):

        return {

            "identifiers": {
                (
                    "biopool",
                    self.unique_id,
                )
            },

            "name": self.name,

            "manufacturer": "BioPoolTech",

            "model": "BioPool Connect",

        }

    @property
    def is_on(self):

        return self.power

    @property
    def is_running(self):

        return self.power

    @property
    def mode_name(self):

        if self.mode is None:
            return None

        return POOL_MODES.get(
            self.mode,
            self.mode,
        )

    @property
    def supports_switch(self):

        return self.definition["switch"]

    @property
    def supports_binary_sensor(self):

        return self.definition["binary_sensor"]

    @property
    def supports_power_sensor(self):

        return self.definition["power_sensor"]

    @property
    def supports_energy_sensor(self):

        return self.definition["energy_sensor"]

    @property
    def supports_runtime_sensor(self):

        return self.definition["runtime_sensor"]

    @property
    def supports_remaining_sensor(self):

        return self.definition["remaining_sensor"]

    def update_from_json(
        self,
        raw: dict,
        data: dict,
    ) -> None:
        """Update this device from controller data."""

        self.mode = self.api.mode

        #
        # Etat
        #
        self.power = (
            str(raw.get("power", "OFF")).upper() == "ON"
        )

        #
        # Puissance
        #
        try:
            self.power_w = float(
                raw.get("sensor-power", 0)
            )
        except (TypeError, ValueError):
            self.power_w = 0

        #
        # Energie
        #
        if not self.supports_power_sensor:

            try:
                self.energy_kwh = float(
                    raw.get("energy", 0)
                )
            except (
                TypeError,
                ValueError,
            ):

                self.energy_kwh = 0.0

        #
        # Valeur "consumed"
        #
        try:
            self.consumed = float(
                raw.get("consumed", 0)
            )
        except (TypeError, ValueError):
            self.consumed = 0

        #
        # Temps de fonctionnement
        #
        if self.function == FUNCTION_PUMP:

            self.runtime_h = round(
                self.consumed,
                1,
            )

        else:

            self.runtime_h = 0

        #
        # Etats "force"
        #
        if self.function == FUNCTION_REACTOR:
            self.force = bool(
                data.get(PARAM_FORCE_UV, False)
            )

        elif self.function == FUNCTION_BACTER:
            self.force = bool(
                data.get(PARAM_FORCE_BACTER, False)
            )

        elif self.function == FUNCTION_OXY:
            self.force = bool(
                data.get(PARAM_FORCE_OXY, False)
            )


class BioPoolAPI:
    """BioPool cloud API."""

    def __init__(
        self,
        hass,
        username,
        password,
        options,
    ):

        self.hass = hass

        self._username = username
        self._password = password

        self._session: ClientSession = (
            async_get_clientsession(hass)
        )

        self._equipment_id: str | None = None

        self.settings = BioPoolSettings(
            options
        )

        self.forced_temperature = None
        self.last_forced_temperature = None

        self._last_energy_update: float | None = None

        #
        # Equipements découverts
        #
        self.devices: dict[str, BioPoolDevice] = {}

        #
        # Dernières données reçues
        #
        self.data: dict = {}

        #
        # Etat global du contrôleur
        #
        self.mode: str | None = None
        self.water_temp: float | None = None
        self.temp_offset: float | None = None

    async def login(self):
        """Authenticate."""

        async with self._session.post(
            f"{BASE_URL}/api/bioservice/login",
            json={
                "username": self._username,
                "password": self._password,
            },
        ) as response:

            response.raise_for_status()

            result = await response.json()

        if not result.get("status"):
            raise RuntimeError(
                "Authentication failed"
            )

        equipments = result["data"].get(
            "equipments",
            [],
        )

        if not equipments:
            raise RuntimeError(
                "No equipment found"
            )

        self._equipment_id = equipments[0]

        _LOGGER.debug(
            "Connected to %s",
            self._equipment_id,
        )

    async def get_data(self):
        """Download latest pool state."""

        if self._equipment_id is None:
            await self.login()

        async with self._session.get(
            f"{BASE_URL}/api/bioconnect/data/"
            f"{self._equipment_id}"
        ) as response:

            response.raise_for_status()

            data = await response.json()

        self.data = data

        #
        # Mode de fonctionnement
        #
        self.mode = str(
            data.get(
                PARAM_MODE,
                "0",
            )
        )

        #
        # Température estimée par le contrôleur
        #
        try:

            self.water_temp = float(
                data.get(
                    "water_temp"
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            self.water_temp = None

        #
        # Offset de température
        #
        try:

            self.temp_offset = float(
                data.get("temp_offset")
            )

        except (
            TypeError,
            ValueError,
        ):

            self.temp_offset = 0.0

        #
        # Mise à jour des équipements
        #
        self._update_devices(data)

        #
        # Calcul de l'énergie
        #
        now = time.monotonic()

        if self._last_energy_update is None:

            #
            # Première lecture :
            # on initialise simplement le chronomètre.
            #
            self._last_energy_update = now

        else:

            elapsed_seconds = (
                now
                - self._last_energy_update
            )

            self._last_energy_update = now

            #
            # Sécurité contre une durée aberrante.
            #
            if (
                elapsed_seconds > 0
                and elapsed_seconds < 3600
            ):

                for device in self.iter_devices():

                    #
                    # L'énergie est calculée uniquement
                    # pour les équipements qui possèdent
                    # un capteur de puissance.
                    #
                    if not device.supports_power_sensor:
                        continue

                    try:

                        power_w = float(
                            device.power_w
                        )

                    except (
                        TypeError,
                        ValueError,
                    ):

                        continue

                    #
                    # Aucun ajout si l'équipement
                    # ne consomme pas.
                    #
                    if power_w <= 0:
                        continue

                    #
                    # W × secondes → kWh
                    #
                    device.energy_kwh += (
                        power_w
                        * elapsed_seconds
                        / 3_600_000
                    )

    async def set_forced_temperature(
        self,
        temperature: float | None,
    ):
        """Set or clear forced water temperature."""

        if temperature is None:

            await self._post_command(
                {
                    PARAM_FORCE_TEMP: None,
                }
            )

        else:

            await self._post_command(
                {
                    PARAM_FORCE_TEMP: f"{temperature:.1f}",
                }
            )

    def get_device(
        self,
        function: str,
    ) -> BioPoolDevice | None:
        """Return one equipment."""

        return self.devices.get(function)

    def iter_devices(self):
        """Iterate through equipments."""

        return self.devices.values()

    def _update_devices(
        self,
        data: dict,
    ) -> None:
        """Update all BioPool devices."""

        for raw in data.get("devices", []):

            function = raw.get("function")

            if function not in DEVICE_DEFINITIONS:
                continue

            device = self.devices.get(function)

            if device is None:

                device = BioPoolDevice(
                    api=self,
                    function=function,
                    device_name=raw["name"],
                )

                self.devices[function] = device

                _LOGGER.debug(
                    "Discovered device %s",
                    function,
                )

            device.update_from_json(
                raw,
                data,
            )

    async def _post_command(
        self,
        params: dict,
    ):
        """Send a generic command."""

        if self._equipment_id is None:
            await self.login()

        #
        # Supprime les paramètres à None.
        # Cela permet par exemple de retirer
        # "force_temp" du contrôleur.
        #
        params = {
            key: value
            for key, value in params.items()
            if value is not None or key == PARAM_FORCE_TEMP
        }

        payload = {
            "db": "true",
            "name": self._equipment_id,
            "params": json.dumps(params),
        }

        _LOGGER.debug("POST command: %s", payload)

        async with self._session.post(
            f"{BASE_URL}/api/bioconnect/command/{self._equipment_id}",
            data=payload,
            headers={
                "Origin": BASE_URL,
                "Referer": (
                    f"{BASE_URL}/app/bioconnect/"
                    f"{self._equipment_id}"
                ),
            },
        ) as response:

            response.raise_for_status()

            try:
                return await response.json()

            except Exception:
                return await response.text()

    async def send_device_command(
        self,
        device: BioPoolDevice,
        command: str,
        value: str,
    ):
        """Send a command to one equipment."""

        trace = {
            "label": (
                "[BioPoolConnect-diags]"
                f"{command}"
            ),
            "infos": {
                "device": device.device_name,
                "cmd": command,
                "val": value,
            },
        }

        payload = {
            "name": device.device_name,
            "cmd": command,
            "val": value,
            "trace": json.dumps(trace),
        }

        async with self._session.post(
            f"{BASE_URL}/api/bioconnect/command/{self._equipment_id}",
            data=payload,
            headers={
                "Content-Type":
                    "application/x-www-form-urlencoded",
                "Origin": BASE_URL,
                "Referer":
                    f"{BASE_URL}/app/bioconnect/{self._equipment_id}",
            },
        ) as response:

            response.raise_for_status()

            try:
                return await response.json()

            except Exception:
                return await response.text()

    async def set_device(
        self,
        function: str,
        state: bool,
    ):
        """Turn one equipment ON/OFF."""

        device = self.get_device(function)

        if device is None:
            raise RuntimeError(
                f"Unknown device '{function}'"
            )

        #
        # Pour l'instant un simple POWER.
        #
        # La logique du mode manuel sera
        # ajoutée ici plus tard.
        #

        await self.send_device_command(
            device,
            CMD_POWER,
            "On" if state else "Off",
        )

        #
        # Mise à jour optimiste
        #
        device.power = state

    async def set_mode(
        self,
        mode: str,
    ):
        """Change pool operating mode."""

        await self._post_command(
            {
                PARAM_MODE: mode,
            }
        )

        self.mode = mode

        #
        # Les équipements héritent du mode.
        #
        for device in self.iter_devices():

            device.mode = mode

    async def set_force(
        self,
        parameter: str,
        enabled: bool,
    ):
        """
        Internal helper.

        Not exposed directly to Home Assistant.
        """

        await self._post_command(
            {
                parameter: enabled,
            }
        )

    async def synchronize_controller(self):
        """Synchronize runtime parameters with the controller."""

        if not self.settings.use_external_temperature:
            return

        if self.forced_temperature is None:
            return

        new_temp = round(
            self.forced_temperature,
            1,
        )

        if new_temp == self.last_forced_temperature:
            return

        await self._post_command(
            {
                PARAM_FORCE_TEMP: f"{new_temp:.1f}",
            }
        )

        self.last_forced_temperature = new_temp

    async def set_temp_offset(
        self,
        value: float,
    ):
        """Change temperature offset."""

        await self._post_command(
            {
                "temp_offset": round(
                    value,
                    1,
                )
            }
        )

        self.temp_offset = round(
            value,
            1,
        )

    async def close(self):
        """Nothing to close."""

        return