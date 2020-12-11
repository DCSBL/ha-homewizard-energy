"""Constants for the Homewizard Energy integration."""

from homeassistant import const

# Set up.
DOMAIN = "homewizard_energy"
PLATFORMS = ["sensor"]

# Platform config.
CONF_ENTITY_ID = const.CONF_ENTITY_ID
CONF_IP_ADDRESS = const.CONF_IP_ADDRESS
CONF_NAME = const.CONF_NAME

# Services.
SERVICE_UPDATE = "update"

# Service attributes.
ATTR_SMR_VERSION = "smr_version"
ATTR_METER_MODEL = "meter_model"
ATTR_WIFI_SSID = "wifi_ssid"
ATTR_WIFI_STRENGTH = "wifi_strength"
ATTR_TOTAL_POWER_IMPORT_T1_KWH = "total_power_import_t1_kwh"
ATTR_TOTAL_POWER_IMPORT_T2_KWH = "total_power_import_t2_kwh"
ATTR_TOTAL_POWER_EXPORT_T1_KWH = "total_power_export_t1_kwh"
ATTR_TOTAL_POWER_EXPORT_T2_KWH = "total_power_export_t2_kwh"
ATTR_ACTIVE_POWER_W = "active_power_w"
ATTR_ACTIVE_POWER_L1_W = "active_power_l1_w"
ATTR_ACTIVE_POWER_L2_W = "active_power_l2_w"
ATTR_ACTIVE_POWER_L3_W = "active_power_l3_w"
ATTR_TOTAL_GAS_M3 = "total_gas_m3"
ATTR_GAS_TIMESTAMP = "gas_timestamp"

# Default values.
DEFAULT_STR_VALUE = "undefined"
DEVICE_DEFAULT_NAME = "P1 Meter"
