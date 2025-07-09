"""Constants for the Dribl integration."""
from datetime import timedelta
from typing import Final

DOMAIN: Final = "dribl"
NAME: Final = "Dribl Football"
MANUFACTURER: Final = "Dribl"

# API Configuration
API_BASE_URL: Final = "https://mc-api.dribl.com/api"
DEFAULT_TENANT: Final = "7MNGJ1QmAz"
DEFAULT_TIMEZONE: Final = "Australia/Hobart"

# Update intervals
DEFAULT_UPDATE_INTERVAL: Final = timedelta(minutes=30)
FAST_UPDATE_INTERVAL: Final = timedelta(minutes=5)

# Configuration
CONF_TENANT_ID: Final = "tenant_id"
CONF_TIMEZONE: Final = "timezone"
CONF_CLUBS: Final = "clubs"
CONF_TEAMS: Final = "teams"
CONF_PLAYERS: Final = "players"
CONF_RESULTS_HOURS: Final = "results_hours"
CONF_UPDATE_INTERVAL: Final = "update_interval"

# Defaults
DEFAULT_RESULTS_HOURS: Final = 72
DEFAULT_UPDATE_INTERVAL_MINUTES: Final = 30

# Sensor types
SENSOR_NEXT_GAME: Final = "next_game"
SENSOR_RECENT_RESULTS: Final = "recent_results"
SENSOR_CLUB_STATS: Final = "club_stats"
SENSOR_PLAYER_STATS: Final = "player_stats"

# Fixture statuses
FIXTURE_STATUS_PENDING: Final = "pending"
FIXTURE_STATUS_COMPLETE: Final = "complete"
FIXTURE_STATUS_CANCELLED: Final = "cancelled"
FIXTURE_STATUS_POSTPONED: Final = "postponed"

# Device classes
DEVICE_CLASS_TIMESTAMP: Final = "timestamp"