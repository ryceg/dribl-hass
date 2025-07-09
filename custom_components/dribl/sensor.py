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
from .const import DOMAIN, MANUFACTURER, NAME, DEFAULT_SUBDOMAIN

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
    
    # Add ladder sensors
    for league_id in coordinator.leagues:
        entities.append(DriblLadderSensor(coordinator, config_entry, league_id))
    
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
    def entity_picture(self) -> Optional[str]:
        """Return entity picture for next game."""
        next_game = self.coordinator.data.get("next_game")
        if not next_game:
            return None
        
        attrs = next_game.get("attributes", {})
        # Use home team logo as entity picture
        return attrs.get("home_logo")

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
    def entity_picture(self) -> Optional[str]:
        """Return entity picture for club."""
        club_data = self.coordinator.data.get("clubs", {}).get(self.club_id, {})
        if not club_data:
            return None
        
        attrs = club_data.get("attributes", {})
        return attrs.get("image")

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
    def entity_picture(self) -> Optional[str]:
        """Return entity picture for player."""
        player_data = self.coordinator.data.get("players", {}).get(self.player_id, {})
        if not player_data:
            return None
        
        attrs = player_data.get("attributes", {})
        return attrs.get("image")

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return extra attributes."""
        player_data = self.coordinator.data.get("players", {}).get(self.player_id, {})
        if not player_data:
            return {}
        
        attrs = player_data.get("attributes", {})
        
        # Get career stats
        career_stats = self.coordinator.data.get("player_careers", {}).get(self.player_id, {})
        
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
            "career_stats": career_stats,
        }


class DriblLadderSensor(DriblSensorEntity):
    """Sensor for league ladder standings."""
    
    def __init__(
        self,
        coordinator: DriblDataUpdateCoordinator,
        config_entry: ConfigEntry,
        league_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, "ladder", league_id)
        self.league_id = league_id
        self._attr_icon = "mdi:format-list-numbered"
        
        # Set name based on league data
        league_name = f"League {league_id}"
        if coordinator.data.get("ladders", {}).get(league_id):
            # Try to get league name from ladder data
            ladder_data = coordinator.data["ladders"][league_id]
            if ladder_data and len(ladder_data) > 0:
                first_entry = ladder_data[0]
                attrs = first_entry.get("attributes", {})
                season_name = attrs.get("season_name", "")
                if season_name:
                    league_name = f"{season_name} Ladder"
        
        self._attr_name = f"Dribl {league_name}"

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        ladder_data = self.coordinator.data.get("ladders", {}).get(self.league_id, [])
        return len(ladder_data)

    @property
    def entity_picture(self) -> Optional[str]:
        """Return entity picture for ladder (top team logo)."""
        ladder_data = self.coordinator.data.get("ladders", {}).get(self.league_id, [])
        if not ladder_data:
            return None
        
        # Use the logo of the team in first position
        first_team = ladder_data[0]
        attrs = first_team.get("attributes", {})
        return attrs.get("club_logo")

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return extra attributes."""
        ladder_data = self.coordinator.data.get("ladders", {}).get(self.league_id, [])
        if not ladder_data:
            return {"ladder": []}
        
        # Get subdomain from config or use default
        subdomain = self.config_entry.data.get("subdomain", DEFAULT_SUBDOMAIN)
        
        formatted_ladder = []
        for entry in ladder_data:
            attrs = entry.get("attributes", {})
            
            # Format recent form with links
            recent_form = []
            recent_matches = attrs.get("recent_matches", [])
            for match in recent_matches[-5:]:  # Last 5 games
                match_id = match.get("match_hash_id")
                home_score = match.get("home_score")
                away_score = match.get("away_score")
                
                # Determine result for this team
                team_hash_id = attrs.get("team_hash_id")
                if team_hash_id == match.get("home_team_hash_id"):
                    # This team was home
                    if home_score is not None and away_score is not None:
                        if home_score > away_score:
                            result = "W"
                        elif home_score < away_score:
                            result = "L"
                        else:
                            result = "D"
                    else:
                        result = "?"
                elif team_hash_id == match.get("away_team_hash_id"):
                    # This team was away
                    if home_score is not None and away_score is not None:
                        if away_score > home_score:
                            result = "W"
                        elif away_score < home_score:
                            result = "L"
                        else:
                            result = "D"
                    else:
                        result = "?"
                else:
                    result = "?"
                
                recent_form.append({
                    "result": result,
                    "link": f"{subdomain}/matchcentre?m={match_id}" if match_id else None,
                    "date": match.get("date"),
                    "home_team": match.get("home_club_name"),
                    "away_team": match.get("away_club_name"),
                    "home_score": home_score,
                    "away_score": away_score,
                })
            
            # Format up next with link
            up_next = None
            upcoming_matches = attrs.get("upcoming_matches", [])
            if upcoming_matches:
                next_match = upcoming_matches[0]
                match_id = next_match.get("match_hash_id")
                up_next = {
                    "link": f"{subdomain}/matchcentre?m={match_id}" if match_id else None,
                    "date": next_match.get("date"),
                    "home_team": next_match.get("home_club_name"),
                    "away_team": next_match.get("away_club_name"),
                    "opponent": next_match.get("away_club_name") if attrs.get("team_hash_id") == next_match.get("home_team_hash_id") else next_match.get("home_club_name"),
                    "home_away": "home" if attrs.get("team_hash_id") == next_match.get("home_team_hash_id") else "away",
                }
            
            formatted_ladder.append({
                "position": attrs.get("position"),
                "team_name": attrs.get("team_name"),
                "club_name": attrs.get("club_name"),
                "club_logo": attrs.get("club_logo"),
                "played": attrs.get("played"),
                "won": attrs.get("won"),
                "drawn": attrs.get("drawn"),
                "lost": attrs.get("lost"),
                "byes": attrs.get("byes"),
                "forfeits": attrs.get("forfeits"),
                "goals_for": attrs.get("goals_for"),
                "goals_against": attrs.get("goals_against"),
                "goal_difference": attrs.get("goal_difference"),
                "points": attrs.get("points"),
                "points_per_game": attrs.get("points_per_game"),
                "recent_form": recent_form,
                "up_next": up_next,
            })
        
        return {
            "ladder": formatted_ladder,
            "team_count": len(formatted_ladder),
        }