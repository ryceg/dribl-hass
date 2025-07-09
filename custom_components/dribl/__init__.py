"""The Dribl integration."""
import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import DriblAPI, DriblAPIError
from .const import (
    CONF_CLUBS,
    CONF_PLAYERS,
    CONF_RESULTS_HOURS,
    CONF_TENANT_ID,
    CONF_TIMEZONE,
    CONF_UPDATE_INTERVAL,
    DEFAULT_RESULTS_HOURS,
    DEFAULT_TENANT,
    DEFAULT_TIMEZONE,
    DEFAULT_UPDATE_INTERVAL_MINUTES,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Dribl from a config entry."""
    session = async_get_clientsession(hass)
    
    # Get configuration
    tenant_id = entry.data.get(CONF_TENANT_ID, DEFAULT_TENANT)
    timezone = entry.data.get(CONF_TIMEZONE, DEFAULT_TIMEZONE)
    clubs = entry.data.get(CONF_CLUBS, [])
    players = entry.data.get(CONF_PLAYERS, [])
    results_hours = entry.options.get(CONF_RESULTS_HOURS, DEFAULT_RESULTS_HOURS)
    update_interval = entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL_MINUTES)
    
    # Create API client
    api = DriblAPI(session, tenant_id, timezone)
    
    # Test connection
    try:
        if not await api.test_connection():
            raise ConfigEntryNotReady("Cannot connect to Dribl API")
    except DriblAPIError as err:
        raise ConfigEntryNotReady(f"Cannot connect to Dribl API: {err}") from err
    
    # Create coordinator
    coordinator = DriblDataUpdateCoordinator(
        hass,
        api,
        clubs,
        players,
        results_hours,
        timedelta(minutes=update_interval),
    )
    
    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()
    
    # Store coordinator
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    
    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Set up options update listener
    entry.async_on_unload(entry.add_update_listener(async_update_options))
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)


class DriblDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: DriblAPI,
        clubs: list,
        players: list,
        results_hours: int,
        update_interval: timedelta,
    ) -> None:
        """Initialize."""
        self.api = api
        self.clubs = clubs
        self.players = players
        self.results_hours = results_hours
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict:
        """Update data via library."""
        try:
            data = {}
            
            # Get next fixtures for followed clubs
            next_fixtures = []
            for club_id in self.clubs:
                fixture = await self.api.get_next_fixture(club=club_id)
                if fixture:
                    next_fixtures.append(fixture)
            
            # Sort by date to get the absolute next game
            if next_fixtures:
                next_fixtures.sort(key=lambda x: x.get("attributes", {}).get("date", ""))
                data["next_game"] = next_fixtures[0]
            else:
                data["next_game"] = None
            
            # Get recent results for followed clubs
            recent_results = []
            for club_id in self.clubs:
                results = await self.api.get_recent_results(
                    hours=self.results_hours,
                    club=club_id
                )
                recent_results.extend(results)
            
            # Sort by date descending (most recent first)
            recent_results.sort(key=lambda x: x.get("attributes", {}).get("date", ""), reverse=True)
            data["recent_results"] = recent_results
            
            # Get club data
            club_data = {}
            if self.clubs:
                all_clubs = await self.api.get_clubs()
                for club in all_clubs:
                    club_id = club.get("id")
                    if club_id in self.clubs:
                        club_data[club_id] = club
            data["clubs"] = club_data
            
            # Get player data
            player_data = {}
            for player_id in self.players:
                profile = await self.api.get_member_profile(player_id)
                if profile:
                    player_data[player_id] = profile
            data["players"] = player_data
            
            return data
            
        except DriblAPIError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err