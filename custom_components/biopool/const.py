from __future__ import annotations

DOMAIN = "biopool"

BASE_URL = "https://bioservice.tech"

MANUFACTURER = "BioPoolTech"
MODEL = "BioPool Connect"

UPDATE_INTERVAL = 60  # secondes

PLATFORMS = [
    "binary_sensor",
    "select",
    "sensor",
    "switch",
    "number",
]

# ------------------------------------------------------------------
# Modes
# ------------------------------------------------------------------

MODE_AUTO = "0"
MODE_FROST = "1"
MODE_OFF = "2"
MODE_MANUAL = "3"

POOL_MODES = {
    MODE_AUTO: "Automatique",
    MODE_FROST: "Hors-gel",
    MODE_OFF: "Arrêt",
    MODE_MANUAL: "Manuel",
}

POOL_MODES_REVERSE = {
    value: key
    for key, value in POOL_MODES.items()
}

# ------------------------------------------------------------------
# Fonctions des équipements
# ------------------------------------------------------------------

FUNCTION_PUMP = "pump"
FUNCTION_REACTOR = "reactor"
FUNCTION_BACTER = "bacter"
FUNCTION_OXY = "oxy"

# ------------------------------------------------------------------
# Commandes
# ------------------------------------------------------------------

CMD_POWER = "POWER"

# ------------------------------------------------------------------
# Paramètres API
# ------------------------------------------------------------------

PARAM_MODE = "mode"

PARAM_FORCE_UV = "force_uv"
PARAM_FORCE_OXY = "force_oxy"
PARAM_FORCE_BACTER = "force_bacter"

PARAM_BACTER_SIZE = "bacter_size"
PARAM_OXY_SIZE = "oxy_size"

PARAM_FORCE_TEMP = "force_temp"

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

CONF_USE_EXTERNAL_TEMPERATURE = "use_external_temperature"
CONF_TEMPERATURE_ENTITY = "temperature_entity"

CONF_BACTER_SIZE = "bacter_size"
CONF_OXY_SIZE = "oxy_size"
CONF_UV_LIFETIME = "uv_lifetime"

# ------------------------------------------------------------------
# Valeurs par défaut
# ------------------------------------------------------------------

DEFAULT_BACTER_SIZE = 5.0      # litres

DEFAULT_OXY_SIZE = 20.0         # litres

DEFAULT_UV_LIFETIME = 8000.0    # heures

# ------------------------------------------------------------------
# Définition des équipements
# ------------------------------------------------------------------

DEVICE_DEFINITIONS = {

    FUNCTION_PUMP: {

        "name": "Pompe filtration",

        "icon": "mdi:water-pump",

        "switch": True,
        "binary_sensor": True,

        "power_sensor": True,
        "energy_sensor": True,
        "runtime_sensor": True,
        "remaining_sensor": False,

    },

    FUNCTION_REACTOR: {

        "name": "Lampe UV",

        "icon": "mdi:lightbulb",

        "switch": True,
        "binary_sensor": True,

        "power_sensor": True,
        "energy_sensor": True,
        "runtime_sensor": False,
        "remaining_sensor": True,

    },

    FUNCTION_BACTER: {

        "name": "Bio-Bacter",

        "icon": "mdi:flask",

        "switch": True,
        "binary_sensor": True,

        "power_sensor": False,
        "energy_sensor": False,
        "runtime_sensor": False,
        "remaining_sensor": True,

    },

    FUNCTION_OXY: {

        "name": "Oxygène actif",

        "icon": "mdi:molecule",

        "switch": True,
        "binary_sensor": True,

        "power_sensor": False,
        "energy_sensor": False,
        "runtime_sensor": False,
        "remaining_sensor": True,

    },

}


SENSOR_WATER_TEMP = "water_temp"

NUMBER_TEMP_OFFSET = "temp_offset"