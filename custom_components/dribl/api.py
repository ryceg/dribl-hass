"""Dribl API client."""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import aiohttp
import async_timeout

from .const import API_BASE_URL, DEFAULT_TENANT, DEFAULT_TIMEZONE

_LOGGER = logging.getLogger(__name__)


class DriblAPIError(Exception):
    """Exception to indicate an API error."""


class DriblAPI:
    """Dribl API client."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        tenant_id: str = DEFAULT_TENANT,
        timezone: str = DEFAULT_TIMEZONE,
    ) -> None:
        """Initialize the API client."""
        self.session = session
        self.tenant_id = tenant_id
        self.timezone = timezone
        self.base_url = API_BASE_URL

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 10,
    ) -> Dict[str, Any]:
        """Make a request to the Dribl API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Add default parameters
        if params is None:
            params = {}
        
        params.update({
            "tenant": self.tenant_id,
            "timezone": self.timezone,
        })

        try:
            async with async_timeout.timeout(timeout):
                async with self.session.request(method, url, params=params) as response:
                    response.raise_for_status()
                    return await response.json()
        except asyncio.TimeoutError as err:
            raise DriblAPIError(f"Request timeout: {url}") from err
        except aiohttp.ClientError as err:
            raise DriblAPIError(f"Request failed: {url} - {err}") from err

    async def get_clubs(self) -> List[Dict[str, Any]]:
        """Get all clubs."""
        try:
            data = await self._request("GET", "/list/clubs", {"disable_paging": "true"})
            return data if isinstance(data, list) else data.get("data", [])
        except DriblAPIError as err:
            _LOGGER.error("Failed to get clubs: %s", err)
            return []

    async def get_leagues(self, competition_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get leagues for a competition."""
        params = {"disable_paging": "true", "sort": "+name"}
        if competition_id:
            params["competition"] = competition_id
        
        try:
            data = await self._request("GET", "/list/leagues", params)
            return data.get("data", []) if isinstance(data, dict) else data
        except DriblAPIError as err:
            _LOGGER.error("Failed to get leagues: %s", err)
            return []

    async def get_fixtures(
        self,
        date_range: str = "default",
        season: Optional[str] = None,
        competition: Optional[str] = None,
        league: Optional[str] = None,
        club: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get fixtures with optional filters."""
        params = {"date_range": date_range}
        
        if season:
            params["season"] = season
        if competition:
            params["competition"] = competition
        if league:
            params["league"] = league
        if club:
            params["club"] = club
        if status:
            params["status"] = status
        
        if date_range == "date_range" and start_date and end_date:
            params["date[]"] = [start_date, end_date]
        elif date_range == "single-date" and start_date:
            params["date"] = start_date

        try:
            data = await self._request("GET", "/fixtures", params)
            return data.get("data", []) if isinstance(data, dict) else []
        except DriblAPIError as err:
            _LOGGER.error("Failed to get fixtures: %s", err)
            return []

    async def get_next_fixture(
        self,
        club: Optional[str] = None,
        team: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Get the next upcoming fixture."""
        today = datetime.now().strftime("%Y-%m-%d")
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        fixtures = await self.get_fixtures(
            date_range="date_range",
            club=club,
            start_date=today,
            end_date=future_date,
            status="pending"
        )
        
        if not fixtures:
            return None
        
        # Sort by date to get the next game
        fixtures.sort(key=lambda x: x.get("attributes", {}).get("date", ""))
        return fixtures[0] if fixtures else None

    async def get_recent_results(
        self,
        hours: int = 72,
        club: Optional[str] = None,
        team: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get recent completed fixtures."""
        end_date = datetime.now()
        start_date = end_date - timedelta(hours=hours)
        
        fixtures = await self.get_fixtures(
            date_range="date_range",
            club=club,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            status="complete"
        )
        
        # Sort by date descending (most recent first)
        fixtures.sort(key=lambda x: x.get("attributes", {}).get("date", ""), reverse=True)
        return fixtures

    async def get_member_profile(self, member_id: str, season: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get member profile information."""
        params = {}
        if season:
            params["season"] = season
        
        try:
            data = await self._request("GET", f"/memberprofile/{member_id}", params)
            return data.get("data") if isinstance(data, dict) else data
        except DriblAPIError as err:
            _LOGGER.error("Failed to get member profile %s: %s", member_id, err)
            return None

    async def get_member_matches(
        self,
        member_id: str,
        season: Optional[str] = None,
        competition: Optional[str] = None,
        league: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get match history for a member."""
        params = {
            "member": member_id,
            "m": member_id,
            "date_range": "default",
        }
        
        if season:
            params["season"] = season
        if competition:
            params["competition"] = competition
        if league:
            params["league"] = league
        
        try:
            data = await self._request("GET", f"/memberprofile-matches/member/{member_id}", params)
            return data.get("data", []) if isinstance(data, dict) else []
        except DriblAPIError as err:
            _LOGGER.error("Failed to get member matches %s: %s", member_id, err)
            return []

    async def get_member_careers(self, member_id: str, season: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get career statistics for a member."""
        params = {"member": member_id}
        if season:
            params["season"] = season
        
        try:
            data = await self._request("GET", f"/memberprofile-careers/member/{member_id}/tenant/{self.tenant_id}", params)
            return data.get("data", []) if isinstance(data, dict) else []
        except DriblAPIError as err:
            _LOGGER.error("Failed to get member careers %s: %s", member_id, err)
            return []

    async def get_match_members(self, match_id: str, team_id: str) -> List[Dict[str, Any]]:
        """Get members for a specific match and team."""
        try:
            data = await self._request("GET", f"/matchcentre-match-members/match/{match_id}/team/{team_id}")
            return data if isinstance(data, list) else []
        except DriblAPIError as err:
            _LOGGER.error("Failed to get match members %s/%s: %s", match_id, team_id, err)
            return []

    async def test_connection(self) -> bool:
        """Test if the API connection is working."""
        try:
            await self.get_clubs()
            return True
        except DriblAPIError:
            return False