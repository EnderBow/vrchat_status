from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up VRChat sensors based on a config entry."""
    coordinators = hass.data[DOMAIN][entry.entry_id]
    vrc_coord = coordinators["vrchat"]
    steam_coord = coordinators["steam"]

    entities = []

    # --- VRChat API Sensors (Mapped to vrc_coord - 1 min updates) ---
    status_components = vrc_coord.data.get("status", {}).get("components", [])
    for comp in status_components:
        entities.append(VRChatStatusSensor(vrc_coord, comp["id"], comp["name"]))

    # Add the total online users sensor
    entities.append(VRChatVisitsSensor(vrc_coord))
    # Add the Steam online users sensor
    entities.append(VRChatSteamOnlineSensor(steam_coord))

    # Add Cloudfront Metric Sensors
    entities.append(VRChatMetricSensor(vrc_coord, "latency", "API Latency", "ms", "mdi:timer-outline"))
    entities.append(VRChatMetricSensor(vrc_coord, "requests", "API Requests", "req/min", "mdi:swap-vertical"))
    entities.append(VRChatMetricSensor(vrc_coord, "errors", "API Errors", "%", "mdi:alert-circle-outline"))
    entities.append(VRChatMetricSensor(vrc_coord, "steam", "Steam Auth Success Rate", "%", "mdi:steam"))
    entities.append(VRChatMetricSensor(vrc_coord, "oculus", "Meta Auth Success Rate", "%", "mdi:virtual-reality"))

    async_add_entities(entities)


class VRChatMetricSensor(CoordinatorEntity, SensorEntity):
    """Representation of a VRChat Cloudfront metric."""
    def __init__(self, coordinator, data_key, name, unit, icon):
        super().__init__(coordinator)
        self._data_key = data_key
        self._attr_name = f"VRChat {name}"
        self._attr_unique_id = f"vrchat_metric_{data_key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        val = self.coordinator.data.get(self._data_key)
        if val is None:
            return None

        # Convert req/ms to req/min (val * 60000)
        if self._data_key == "requests":
            return round(float(val) * 60000, 2)

        # Convert error decimal (e.g., 3.2e-06) to percentage
        if self._data_key == "errors":
            return round(float(val) * 100, 5)

        # Auth Success: Convert ratio (e.g., 0.96) to percentage (96.38%)
        if self._data_key in ["steam", "oculus"]:
            return round(float(val) * 100, 2)

        return round(float(val), 3)


class VRChatStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a VRChat Status component sensor."""
    def __init__(self, coordinator, comp_id, name):
        super().__init__(coordinator)
        self._comp_id = comp_id
        self._attr_name = f"VRChat {name}"
        self._attr_unique_id = f"vrchat_{comp_id}"

    @property
    def native_value(self):
        # Access data through the 'status' key now
        components = self.coordinator.data.get("status", {}).get("components", [])
        component = next((c for c in components if c["id"] == self._comp_id), None)
        return component["status"] if component else "unknown"


class VRChatVisitsSensor(CoordinatorEntity, SensorEntity):
    """Representation of the total amount of Online VRChat Users."""
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "VRChat Online Users"
        self._attr_unique_id = "vrchat_online_users"
        self._attr_icon = "mdi:account-multiple"

        # This makes it show as a line graph in the UI
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "users"

    @property
    def native_value(self):
        return self.coordinator.data.get("online_users")


class VRChatSteamOnlineSensor(CoordinatorEntity, SensorEntity):
    """Representation of VRChat players currently on Steam."""
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "VRChat Steam Online Users"
        self._attr_unique_id = "vrchat_steam_online_users"
        self._attr_icon = "mdi:steam"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "users"

    @property
    def native_value(self):
        # Pulling the renamed key from your dictionary
        return self.coordinator.data.get("steam_online_users")