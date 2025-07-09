"""Sensor platform for Dribl integration."""
import logging
from datetime import datetime
from typing import Any, Dict, Optional
from urllib.parse import quote

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from . import DriblDataUpdateCoordinator
from .const import DOMAIN, MANUFACTURER, NAME

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Dribl sensors."""
    coordinator: DriblDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = [
        DriblNextGameSensor(coordinator, config_entry),
        DriblRecentResultsSensor(coordinator, config_entry),
    ]
    
    # Add club sensors
    for club_id in coordinator.clubs:
        entities.append(DriblClubSensor(coordinator, config_entry, club_id))
    
    # Add player sensors
    for player_id in coordinator.players:
        entities.append(DriblPlayerSensor(coordinator, config_entry, player_id))
    
    async_add_entities(entities)


class DriblSensorEntity(CoordinatorEntity, SensorEntity):
    """Base class for Dribl sensors."""
    
    def __init__(
        self,
        coordinator: DriblDataUpdateCoordinator,
        config_entry: ConfigEntry,
        sensor_type: str,
        identifier: Optional[str] = None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.sensor_type = sensor_type
        self.identifier = identifier
        
        # Set unique ID
        if identifier:
            self._attr_unique_id = f"{config_entry.entry_id}_{sensor_type}_{identifier}"
        else:
            self._attr_unique_id = f"{config_entry.entry_id}_{sensor_type}"
        
        # Set device info
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": NAME,
            "manufacturer": MANUFACTURER,
            "model": "Dribl Integration",
            "sw_version": "1.0.0",
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success


class DriblNextGameSensor(DriblSensorEntity):
    """Sensor for next scheduled game."""
    
    def __init__(
        self,
        coordinator: DriblDataUpdateCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, "next_game")
        self._attr_name = "Dribl Next Game"
        self._attr_icon = "mdi:soccer"

    @property
    def state(self) -> Optional[str]:
        """Return the state of the sensor."""
        next_game = self.coordinator.data.get("next_game")
        if not next_game:
            return "No upcoming games"
        
        game_date = next_game.get("attributes", {}).get("date")
        if not game_date:
            return "Unknown"
        
        try:
            # Parse the date string
            dt = datetime.fromisoformat(game_date.replace('Z', '+00:00'))
            # Convert to local time
            local_dt = dt_util.as_local(dt)
            return local_dt.strftime("%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            return "Unknown"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return extra attributes."""
        next_game = self.coordinator.data.get("next_game")
        if not next_game:
            return {}
        
        attrs = next_game.get("attributes", {})
        
        # Create Google Maps link
        maps_link = None
        if attrs.get("ground_latitude") and attrs.get("ground_longitude"):
            lat = attrs["ground_latitude"]
            lng = attrs["ground_longitude"]
            ground_name = attrs.get("ground_name", "")
            if ground_name:
                query = quote(f"{ground_name}")
                maps_link = f"https://maps.google.com/?q={query}@{lat},{lng}"
            else:
                maps_link = f"https://maps.google.com/?q={lat},{lng}"
        
        return {
            "home_team": attrs.get("home_team_name"),
            "away_team": attrs.get("away_team_name"),
            "home_logo": attrs.get("home_logo"),
            "away_logo": attrs.get("away_logo"),
            "ground_name": attrs.get("ground_name"),
            "field_name": attrs.get("field_name"),
            "competition": attrs.get("competition_name"),
            "league": attrs.get("league_name"),
            "round": attrs.get("full_round"),
            "status": attrs.get("status"),
            "google_maps_link": maps_link,
            "ground_address": attrs.get("ground_address"),
            "match_name": attrs.get("name"),
        }


class DriblRecentResultsSensor(DriblSensorEntity):
    """Sensor for recent game results."""
    
    def __init__(
        self,
        coordinator: DriblDataUpdateCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, "recent_results")
        self._attr_name = "Dribl Recent Results"
        self._attr_icon = "mdi:soccer-field"

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        results = self.coordinator.data.get("recent_results", [])
        return len(results)

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return extra attributes."""
        results = self.coordinator.data.get("recent_results", [])
        
        if not results:
            return {"results": []}
        
        formatted_results = []
        for result in results:
            attrs = result.get("attributes", {})
            
            # Format the date
            game_date = attrs.get("date")
            formatted_date = "Unknown"
            if game_date:
                try:
                    dt = datetime.fromisoformat(game_date.replace('Z', '+00:00'))
                    local_dt = dt_util.as_local(dt)
                    formatted_date = local_dt.strftime("%Y-%m-%d %H:%M")
                except (ValueError, TypeError):
                    pass
            
            formatted_results.append({
                "date": formatted_date,
                "home_team": attrs.get("home_team_name"),
                "away_team": attrs.get("away_team_name"),
                "home_score": attrs.get("home_score"),
                "away_score": attrs.get("away_score"),
                "home_logo": attrs.get("home_logo"),
                "away_logo": attrs.get("away_logo"),
                "competition": attrs.get("competition_name"),
                "league": attrs.get("league_name"),
                "round": attrs.get("full_round"),
                "ground_name": attrs.get("ground_name"),
                "status": attrs.get("status"),
            })
        
        return {
            "results": formatted_results,
            "count": len(formatted_results),
        }


class DriblClubSensor(DriblSensorEntity):
    """Sensor for club information."""
    
    def __init__(
        self,
        coordinator: DriblDataUpdateCoordinator,
        config_entry: ConfigEntry,
        club_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, "club", club_id)
        self.club_id = club_id
        self._attr_icon = "mdi:shield-star"
        
        # Set name based on club data
        club_data = coordinator.data.get("clubs", {}).get(club_id, {})
        club_name = club_data.get("attributes", {}).get("name", f"Club {club_id}")
        self._attr_name = f"Dribl {club_name}"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        club_data = self.coordinator.data.get("clubs", {}).get(self.club_id, {})
        if not club_data:
            return "Unknown"
        
        return club_data.get("attributes", {}).get("name", "Unknown")

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return extra attributes."""
        club_data = self.coordinator.data.get("clubs", {}).get(self.club_id, {})
        if not club_data:
            return {}
        
        attrs = club_data.get("attributes", {})
        
        return {
            "club_id": self.club_id,
            "name": attrs.get("name"),
            "image": attrs.get("image"),
            "email": attrs.get("email"),
            "phone": attrs.get("phone"),
            "website": attrs.get("url"),
            "color": attrs.get("color"),
            "accent_color": attrs.get("accent"),
            "address": attrs.get("address", {}),
            "socials": attrs.get("socials", []),
        }


class DriblPlayerSensor(DriblSensorEntity):
    """Sensor for player information."""
    
    def __init__(
        self,
        coordinator: DriblDataUpdateCoordinator,
        config_entry: ConfigEntry,
        player_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, "player", player_id)
        self.player_id = player_id
        self._attr_icon = "mdi:account-circle"
        
        # Set name based on player data
        player_data = coordinator.data.get("players", {}).get(player_id, {})
        attrs = player_data.get("attributes", {})
        player_name = f"{attrs.get('first_name', '')} {attrs.get('last_name', '')}".strip()
        if not player_name:
            player_name = f"Player {player_id}"
        self._attr_name = f"Dribl {player_name}"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        player_data = self.coordinator.data.get("players", {}).get(self.player_id, {})
        if not player_data:
            return "Unknown"
        
        attrs = player_data.get("attributes", {})
        first_name = attrs.get("first_name", "")
        last_name = attrs.get("last_name", "")
        
        return f"{first_name} {last_name}".strip() or "Unknown"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return extra attributes."""
        player_data = self.coordinator.data.get("players", {}).get(self.player_id, {})
        if not player_data:
            return {}
        
        attrs = player_data.get("attributes", {})
        
        return {
            "player_id": self.player_id,
            "first_name": attrs.get("first_name"),
            "last_name": attrs.get("last_name"),
            "image": attrs.get("image"),
            "age": attrs.get("age"),
            "nationality": attrs.get("nationality"),
            "is_captain": attrs.get("is_captain"),
            "is_goalkeeper": attrs.get("is_goalkeeper"),
            "clubs": attrs.get("player_clubs", []),
            "club_color": attrs.get("club_color"),
            "club_accent": attrs.get("club_accent"),
        }