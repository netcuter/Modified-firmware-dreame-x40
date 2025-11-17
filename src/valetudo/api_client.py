"""Valetudo REST API Client"""

import httpx
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RobotStatus:
    """Robot status data"""
    state: str
    battery: int
    error: Optional[str] = None


@dataclass
class RobotCapability:
    """Robot capability"""
    type: str
    enabled: bool


class ValetudoAPIClient:
    """Client for Valetudo REST API"""

    def __init__(self, base_url: str, timeout: int = 10):
        """Initialize Valetudo API client

        Args:
            base_url: Base URL of Valetudo API (e.g., http://192.168.1.100/api/v2)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
        logger.info(f"Initialized Valetudo API client: {base_url}")

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

    async def _get(self, endpoint: str) -> Dict[str, Any]:
        """Make GET request to Valetudo API

        Args:
            endpoint: API endpoint (without base URL)

        Returns:
            JSON response as dict
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"GET {url}")

        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise

    async def _put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make PUT request to Valetudo API

        Args:
            endpoint: API endpoint
            data: JSON data to send

        Returns:
            JSON response as dict
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"PUT {url} with data: {data}")

        try:
            response = await self.client.put(url, json=data)
            response.raise_for_status()
            return response.json() if response.text else {}
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise

    # ===== Robot Status =====

    async def get_robot_info(self) -> Dict[str, Any]:
        """Get robot information"""
        return await self._get("robot")

    async def get_capabilities(self) -> List[Dict[str, Any]]:
        """Get robot capabilities"""
        data = await self._get("robot/capabilities")
        return data

    async def get_state(self) -> Dict[str, Any]:
        """Get current robot state"""
        return await self._get("robot/state")

    async def get_battery_state(self) -> Dict[str, Any]:
        """Get battery state"""
        try:
            return await self._get("robot/capabilities/BatteryStateCapability")
        except:
            # Fallback to state
            state = await self.get_state()
            return state.get("battery", {})

    # ===== Map =====

    async def get_map(self) -> Dict[str, Any]:
        """Get current map data"""
        return await self._get("robot/capabilities/MapSegmentationCapability")

    async def get_segments(self) -> List[Dict[str, Any]]:
        """Get map segments (rooms)"""
        map_data = await self.get_map()
        return map_data.get("segments", [])

    # ===== Cleaning Commands =====

    async def start_cleaning(self) -> Dict[str, Any]:
        """Start full cleaning"""
        return await self._put("robot/capabilities/BasicControlCapability", {
            "action": "start"
        })

    async def stop_cleaning(self) -> Dict[str, Any]:
        """Stop cleaning"""
        return await self._put("robot/capabilities/BasicControlCapability", {
            "action": "stop"
        })

    async def pause_cleaning(self) -> Dict[str, Any]:
        """Pause cleaning"""
        return await self._put("robot/capabilities/BasicControlCapability", {
            "action": "pause"
        })

    async def return_to_dock(self) -> Dict[str, Any]:
        """Return robot to dock"""
        return await self._put("robot/capabilities/BasicControlCapability", {
            "action": "home"
        })

    async def locate_robot(self) -> Dict[str, Any]:
        """Play locate sound"""
        return await self._put("robot/capabilities/LocateCapability", {
            "action": "locate"
        })

    async def clean_segments(self, segment_ids: List[str], iterations: int = 1) -> Dict[str, Any]:
        """Clean specific segments (rooms)

        Args:
            segment_ids: List of segment IDs to clean
            iterations: Number of cleaning iterations

        Returns:
            API response
        """
        return await self._put("robot/capabilities/MapSegmentationCapability", {
            "action": "start_segment_action",
            "segment_ids": segment_ids,
            "iterations": iterations,
            "customOrder": True
        })

    async def clean_zone(self, zones: List[Dict[str, int]], iterations: int = 1) -> Dict[str, Any]:
        """Clean specific zones

        Args:
            zones: List of zone coordinates [{"x1": x1, "y1": y1, "x2": x2, "y2": y2}]
            iterations: Number of cleaning iterations

        Returns:
            API response
        """
        return await self._put("robot/capabilities/ZoneCleaningCapability", {
            "action": "clean",
            "zones": zones,
            "iterations": iterations
        })

    # ===== Fan Speed =====

    async def get_fan_speed(self) -> Dict[str, Any]:
        """Get current fan speed"""
        return await self._get("robot/capabilities/FanSpeedControlCapability")

    async def set_fan_speed(self, level: str) -> Dict[str, Any]:
        """Set fan speed level

        Args:
            level: Fan speed level (e.g., "off", "min", "low", "medium", "high", "max", "turbo")

        Returns:
            API response
        """
        return await self._put("robot/capabilities/FanSpeedControlCapability", {
            "preset": level
        })

    # ===== Water Usage =====

    async def get_water_usage(self) -> Dict[str, Any]:
        """Get current water usage level"""
        return await self._get("robot/capabilities/WaterUsageControlCapability")

    async def set_water_usage(self, level: str) -> Dict[str, Any]:
        """Set water usage level

        Args:
            level: Water usage level (e.g., "off", "min", "low", "medium", "high", "max")

        Returns:
            API response
        """
        return await self._put("robot/capabilities/WaterUsageControlCapability", {
            "preset": level
        })

    # ===== Consumables =====

    async def get_consumables(self) -> Dict[str, Any]:
        """Get consumables status (filter, brushes, etc.)"""
        return await self._get("robot/capabilities/ConsumableMonitoringCapability")

    # ===== Convenience Methods =====

    async def get_friendly_status(self) -> RobotStatus:
        """Get user-friendly robot status

        Returns:
            RobotStatus object with state, battery, and error
        """
        state = await self.get_state()
        battery = await self.get_battery_state()

        return RobotStatus(
            state=state.get("state", "unknown"),
            battery=battery.get("level", 0),
            error=state.get("error")
        )

    async def is_cleaning(self) -> bool:
        """Check if robot is currently cleaning"""
        state = await self.get_state()
        return state.get("state") in ["cleaning", "moving"]

    async def is_docked(self) -> bool:
        """Check if robot is docked"""
        state = await self.get_state()
        return state.get("state") == "docked"
