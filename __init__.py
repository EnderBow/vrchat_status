import logging
import async_timeout
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_URL_STATUS, CONF_URL_VISITS, CONF_URL_LATENCY, CONF_URL_REQUESTS, CONF_URL_ERRORS, CONF_URL_STEAM, CONF_URL_OCULUS, CONF_URL_STEAM_STATS

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up VRChat Status from a config entry."""
    session = async_get_clientsession(hass)

    async def async_update_data():
        async with async_timeout.timeout(10):
            # Fetch Status Page Data
            async with session.get(CONF_URL_STATUS) as resp:
                status_data = await resp.json()
            async with session.get(CONF_URL_VISITS) as resp:
                text_data = await resp.text()
                try:
                    online_users = int(text_data.strip())
                except ValueError:
                    online_users = 0

            # Get latest metrics from Cloudfront URLs
            async def get_latest_metric(url):
                try:
                    async with session.get(url) as resp:
                        data = await resp.json()
                        if data and isinstance(data, list):
                            return data[-1][1]  # Get last list item, then the value
                except Exception as err:
                    _LOGGER.error("Error fetching %s: %s", url, err)
                return 0

            # Fetch Steam Player Count
            steam_players = 0
            try:
                async with session.get(CONF_URL_STEAM_STATS) as resp:
                    steam_data = await resp.json()
                    steam_players = steam_data.get("response", {}).get("player_count", 0)
            except Exception as err:
                _LOGGER.error("Error fetching Steam player count: %s", err)

            return {
                "status": status_data,
                "online_users": online_users,
                "steam_online_users": steam_players,
                "latency": await get_latest_metric(CONF_URL_LATENCY),
                "requests": await get_latest_metric(CONF_URL_REQUESTS),
                "errors": await get_latest_metric(CONF_URL_ERRORS),
                "steam": await get_latest_metric(CONF_URL_STEAM),
                "oculus": await get_latest_metric(CONF_URL_OCULUS),
            }

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_interval=timedelta(minutes=1),
        update_method=async_update_data,
    )

    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # This tells HA to look at sensor.py for entities
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok