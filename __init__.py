import logging
import async_timeout
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_URL_STATUS, CONF_URL_VISITS, CONF_URL_LATENCY, CONF_URL_REQUESTS, CONF_URL_ERRORS, CONF_URL_STEAM, CONF_URL_OCULUS, CONF_URL_STEAM_STATS

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    session = async_get_clientsession(hass)

    # --- COORDINATOR 1: VRChat (1 Minute) ---
    async def async_update_vrchat():
        try:
            async with async_timeout.timeout(10):
                async with session.get(CONF_URL_STATUS) as resp:
                    resp.raise_for_status() # crashes if status is 404/500
                    status_data = await resp.json()
                async with session.get(CONF_URL_VISITS) as resp:
                    resp.raise_for_status() # crashes if status is 404/500
                    text_data = await resp.text()
                    online_users = int(text_data.strip()) if text_data.strip().isdigit() else 0

                # Metric helper
                async def get_metric(url):
                    try:
                        async with session.get(url) as resp:
                            data = await resp.json()
                            return data[-1][1] if data else 0
                    except Exception: return 0

                return {
                    "status": status_data,
                    "online_users": online_users,
                    "latency": await get_metric(CONF_URL_LATENCY),
                    "requests": await get_metric(CONF_URL_REQUESTS),
                    "errors": await get_metric(CONF_URL_ERRORS),
                    "steam": await get_metric(CONF_URL_STEAM),
                    "oculus": await get_metric(CONF_URL_OCULUS),
                }
        except Exception as err:
            _LOGGER.error("VRChat update failed: %s", err)
            raise UpdateFailed(f"VRChat API error: {err}")

    vrchat_coordinator = DataUpdateCoordinator(
        hass, _LOGGER, name=f"{DOMAIN}_vrchat",
        update_interval=timedelta(minutes=1),
        update_method=async_update_vrchat,
    )

    # --- COORDINATOR 2: Steam (5 Minutes) ---
    async def async_update_steam():
        try:
            async with async_timeout.timeout(10):
                async with session.get(CONF_URL_STEAM_STATS) as resp:
                    resp.raise_for_status() # crashes if status is 404/500
                    data = await resp.json()
                    return {"steam_online_users": data.get("response", {}).get("player_count", 0)}
        except Exception as err:
            _LOGGER.error("Steam update failed: %s", err)
            raise UpdateFailed(f"Network error: {err}")

    steam_coordinator = DataUpdateCoordinator(
        hass, _LOGGER, name=f"{DOMAIN}_steam",
        update_interval=timedelta(minutes=5),
        update_method=async_update_steam,
    )

    # Refresh both and store them
    await vrchat_coordinator.async_config_entry_first_refresh()
    await steam_coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "vrchat": vrchat_coordinator,
        "steam": steam_coordinator
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok