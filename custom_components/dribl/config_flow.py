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
    
    # Get available clubs for selection
    clubs = await api.get_clubs()
    
    return {
        "title": NAME,
        "clubs": clubs,
    }


class DriblConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Dribl."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.data: Dict[str, Any] = {}
        self.clubs: list = []
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
                self.clubs = info["clubs"]
                
                # Move to club selection step
                return await self.async_step_clubs()
                
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

    async def async_step_clubs(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle club selection."""
        if user_input is not None:
            self.data[CONF_CLUBS] = user_input.get(CONF_CLUBS, [])
            return await self.async_step_players()
        
        # Create club options
        club_options = {}
        for club in self.clubs:
            club_id = club.get("id")
            club_name = club.get("attributes", {}).get("name", "Unknown Club")
            if club_id:
                club_options[club_id] = club_name
        
        return self.async_show_form(
            step_id="clubs",
            data_schema=vol.Schema({
                vol.Optional(CONF_CLUBS, default=[]): cv.multi_select(club_options),
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