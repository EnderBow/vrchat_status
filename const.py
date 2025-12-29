"""Constants for the VRChat Status integration."""

# The domain of your component.
# This must match the folder name and the domain in manifest.json.
DOMAIN = "vrchat_status"

# API URLs
CONF_URL_STATUS = "https://status.vrchat.com/api/v2/summary.json"
CONF_URL_VISITS = "https://api.vrchat.cloud/api/1/visits"

# Cloudfront Metrics
CONF_URL_LATENCY = "https://d31qqo63tn8lj0.cloudfront.net/apilatency.json"
CONF_URL_REQUESTS = "https://d31qqo63tn8lj0.cloudfront.net/apirequests.json"
CONF_URL_ERRORS = "https://d31qqo63tn8lj0.cloudfront.net/apierrors.json"
CONF_URL_STEAM = "https://d31qqo63tn8lj0.cloudfront.net/extauth_steam.json"
CONF_URL_OCULUS = "https://d31qqo63tn8lj0.cloudfront.net/extauth_oculus.json"

# Steam Players API URL
CONF_URL_STEAM_STATS ="https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=438100"

# Update interval
DEFAULT_SCAN_INTERVAL = 60 # 1 minute