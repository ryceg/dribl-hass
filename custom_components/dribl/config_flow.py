"""Config flow for Dribl integration."""
import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .api import DriblAPI, DriblAPIError
from .const import (
    CONF_CLUBS,
    CONF_COMPETITIONS,
    CONF_GROUNDS,
    CONF_LEAGUES,
    CONF_PLAYERS,
    CONF_RESULTS_HOURS,
    CONF_ROUNDS,
    CONF_SEASON,
    CONF_TENANT_ID,
    CONF_TIMEZONE,
    CONF_UPDATE_INTERVAL,
    DEFAULT_RESULTS_HOURS,
    DEFAULT_TENANT,
    DEFAULT_TIMEZONE,
    DEFAULT_UPDATE_INTERVAL_MINUTES,
    DOMAIN,
    NAME,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_TENANT_ID, default=DEFAULT_TENANT): cv.string,
        vol.Required(CONF_TIMEZONE, default=DEFAULT_TIMEZONE): cv.string,
        vol.Optional(CONF_RESULTS_HOURS, default=DEFAULT_RESULTS_HOURS): vol.All(
            vol.Coerce(int), vol.Clamp(min=1, max=168)
        ),
        vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL_MINUTES): vol.All(
            vol.Coerce(int), vol.Range(min=5, max=1440)
        ),
    }
)


async def validate_input(hass: HomeAssistant, data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate the user input allows us to connect."""
    session = async_get_clientsession(hass)
    api = DriblAPI(session, data[CONF_TENANT_ID], data[CONF_TIMEZONE])
    
    if not await api.test_connection():
        raise DriblAPIError("Cannot connect to Dribl API")
    
    # Get available seasons for selection
    seasons = await api.get_seasons()
    _LOGGER.debug("Retrieved seasons from API: %s", seasons)
    
    return {
        "title": NAME,
        "seasons": seasons,
    }


class DriblConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Dribl."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.data: Dict[str, Any] = {}
        self.seasons: list = []
        self.competitions: list = []
        self.leagues: list = []
        self.clubs: list = []
        self.rounds: list = []
        self.grounds: list = []
        self.players: list = []

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}
        
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                self.data.update(user_input)
                self.seasons = info["seasons"]
                
                # Move to season selection step
                return await self.async_step_season()
                
            except DriblAPIError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_season(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle season selection."""
        if user_input is not None:
            self.data[CONF_SEASON] = user_input.get(CONF_SEASON)
            return await self.async_step_competitions()
        
        # Create season options
        season_options = {}
        _LOGGER.debug("Available seasons: %s", self.seasons)
        for season in self.seasons:
            season_id = season.get("id") or season.get("value")
            season_name = season.get("name") or season.get("title", "Unknown Season")
            _LOGGER.debug("Processing season: id=%s, name=%s", season_id, season_name)
            if season_id:
                season_options[season_id] = season_name
        _LOGGER.debug("Season options: %s", season_options)
        
        return self.async_show_form(
            step_id="season",
            data_schema=vol.Schema({
                vol.Required(CONF_SEASON): vol.In(season_options if season_options else {"no_seasons": "No seasons available"}),
            }),
        )

    async def async_step_competitions(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle competition selection."""
        if user_input is not None:
            self.data[CONF_COMPETITIONS] = user_input.get(CONF_COMPETITIONS, [])
            return await self.async_step_leagues()
        
        # Get competitions for selected season
        try:
            session = async_get_clientsession(self.hass)
            api = DriblAPI(session, self.data[CONF_TENANT_ID], self.data[CONF_TIMEZONE])
            competitions = await api.get_competitions(self.data.get(CONF_SEASON))
            self.competitions = competitions
        except Exception as e:
            _LOGGER.error("Failed to get competitions: %s", e)
            competitions = []
        
        # Create competition options
        competition_options = {}
        for competition in competitions:
            comp_id = competition.get("id") or competition.get("value")
            comp_name = competition.get("name") or competition.get("title", "Unknown Competition")
            if comp_id:
                competition_options[comp_id] = comp_name
        
        return self.async_show_form(
            step_id="competitions",
            data_schema=vol.Schema({
                vol.Optional(CONF_COMPETITIONS, default=[]): cv.multi_select(competition_options if competition_options else {"no_competitions": "No competitions available"}),
            }),
        )

    async def async_step_leagues(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle league selection."""
        if user_input is not None:
            self.data[CONF_LEAGUES] = user_input.get(CONF_LEAGUES, [])
            return await self.async_step_clubs()
        
        # Get leagues for selected competitions
        try:
            session = async_get_clientsession(self.hass)
            api = DriblAPI(session, self.data[CONF_TENANT_ID], self.data[CONF_TIMEZONE])
            leagues = []
            for comp_id in self.data.get(CONF_COMPETITIONS, []):
                comp_leagues = await api.get_leagues(comp_id)
                leagues.extend(comp_leagues)
            self.leagues = leagues
        except Exception as e:
            _LOGGER.error("Failed to get leagues: %s", e)
            leagues = []
        
        # Create league options
        league_options = {}
        for league in leagues:
            league_id = league.get("id") or league.get("value")
            league_name = league.get("name") or league.get("title", "Unknown League")
            if league_id:
                league_options[league_id] = league_name
        
        return self.async_show_form(
            step_id="leagues",
            data_schema=vol.Schema({
                vol.Optional(CONF_LEAGUES, default=[]): cv.multi_select(league_options if league_options else {"no_leagues": "No leagues available"}),
            }),
        )

    async def async_step_clubs(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle club selection."""
        if user_input is not None:
            self.data[CONF_CLUBS] = user_input.get(CONF_CLUBS, [])
            return await self.async_step_rounds()
        
        # Get clubs
        try:
            session = async_get_clientsession(self.hass)
            api = DriblAPI(session, self.data[CONF_TENANT_ID], self.data[CONF_TIMEZONE])
            clubs = await api.get_clubs()
            self.clubs = clubs
        except Exception as e:
            _LOGGER.error("Failed to get clubs: %s", e)
            clubs = []
        
        # Create club options
        club_options = {}
        _LOGGER.debug("Available clubs: %s", self.clubs)
        for club in self.clubs:
            club_id = club.get("id")
            club_attrs = club.get("attributes", {})
            club_name = club_attrs.get("name", "Unknown Club")
            club_image = club_attrs.get("image")
            _LOGGER.debug("Processing club: id=%s, name=%s, image=%s", club_id, club_name, club_image)
            if club_id:
                # Add logo emoji or indicator if image exists
                display_name = f"🏆 {club_name}" if club_image else club_name
                club_options[club_id] = display_name
        _LOGGER.debug("Club options: %s", club_options)
        
        return self.async_show_form(
            step_id="clubs",
            data_schema=vol.Schema({
                vol.Optional(CONF_CLUBS, default=[]): cv.multi_select(club_options if club_options else {"no_clubs": "No clubs available"}),
            }),
        )

    async def async_step_rounds(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle round selection."""
        if user_input is not None:
            self.data[CONF_ROUNDS] = user_input.get(CONF_ROUNDS, [])
            return await self.async_step_grounds()
        
        # Get rounds for selected season and competitions
        try:
            session = async_get_clientsession(self.hass)
            api = DriblAPI(session, self.data[CONF_TENANT_ID], self.data[CONF_TIMEZONE])
            rounds = []
            for comp_id in self.data.get(CONF_COMPETITIONS, []):
                comp_rounds = await api.get_rounds(self.data.get(CONF_SEASON), comp_id)
                rounds.extend(comp_rounds)
            self.rounds = rounds
        except Exception as e:
            _LOGGER.error("Failed to get rounds: %s", e)
            rounds = []
        
        # Create round options
        round_options = {}
        for round_data in rounds:
            round_id = round_data.get("value")
            round_name = round_data.get("name") or round_data.get("title", "Unknown Round")
            if round_id:
                round_options[round_id] = round_name
        
        return self.async_show_form(
            step_id="rounds",
            data_schema=vol.Schema({
                vol.Optional(CONF_ROUNDS, default=[]): cv.multi_select(round_options if round_options else {"no_rounds": "No rounds available"}),
            }),
        )

    async def async_step_grounds(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle ground selection."""
        if user_input is not None:
            self.data[CONF_GROUNDS] = user_input.get(CONF_GROUNDS, [])
            return await self.async_step_players()
        
        # Get grounds for selected season and competitions
        try:
            session = async_get_clientsession(self.hass)
            api = DriblAPI(session, self.data[CONF_TENANT_ID], self.data[CONF_TIMEZONE])
            grounds = []
            for comp_id in self.data.get(CONF_COMPETITIONS, []):
                comp_grounds = await api.get_grounds(self.data.get(CONF_SEASON), comp_id)
                grounds.extend(comp_grounds)
            self.grounds = grounds
        except Exception as e:
            _LOGGER.error("Failed to get grounds: %s", e)
            grounds = []
        
        # Create ground options
        ground_options = {}
        for ground in grounds:
            ground_id = ground.get("id") or ground.get("value")
            ground_name = ground.get("name") or ground.get("title", "Unknown Ground")
            if ground_id:
                ground_options[ground_id] = ground_name
        
        return self.async_show_form(
            step_id="grounds",
            data_schema=vol.Schema({
                vol.Optional(CONF_GROUNDS, default=[]): cv.multi_select(ground_options if ground_options else {"no_grounds": "No grounds available"}),
            }),
        )

    async def async_step_players(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle player selection."""
        if user_input is not None:
            # For now, allow manual entry of player IDs
            player_input = user_input.get("player_ids", "")
            if player_input:
                # Split by comma and clean up
                player_ids = [p.strip() for p in player_input.split(",") if p.strip()]
                self.data[CONF_PLAYERS] = player_ids
            else:
                self.data[CONF_PLAYERS] = []
            
            # Create the config entry
            return self.async_create_entry(
                title=NAME,
                data=self.data,
            )
        
        # Allow manual entry of player IDs (comma-separated)
        return self.async_show_form(
            step_id="players",
            data_schema=vol.Schema({
                vol.Optional("player_ids", default=""): cv.string,
            }),
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return DriblOptionsFlowHandler(config_entry)


class DriblOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Dribl."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_RESULTS_HOURS,
                        default=self.config_entry.options.get(
                            CONF_RESULTS_HOURS, DEFAULT_RESULTS_HOURS
                        ),
                    ): vol.All(vol.Coerce(int), vol.Clamp(min=1, max=168)),
                    vol.Optional(
                        CONF_UPDATE_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL_MINUTES
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=5, max=1440)),
                }
            ),
        )