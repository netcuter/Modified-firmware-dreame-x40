"""User tracking module - tracks user position for follow-me mode"""

import logging
import asyncio
from typing import Optional, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class UserTracker:
    """Tracks user position for follow-me functionality"""

    def __init__(self):
        self.user_position: Optional[Tuple[int, int]] = None
        self.last_update: Optional[datetime] = None
        self.follow_mode_active: bool = False
        self.follow_distance: int = 500  # mm - minimum distance to follow
        self.update_interval: float = 2.0  # seconds

    def update_position(self, x: int, y: int):
        """Update user's current position

        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.user_position = (x, y)
        self.last_update = datetime.now()
        logger.debug(f"User position updated: ({x}, {y})")

    def get_position(self) -> Optional[Tuple[int, int]]:
        """Get last known user position

        Returns:
            Tuple of (x, y) or None if no recent position
        """
        # Position is valid for 10 seconds
        if self.last_update and (datetime.now() - self.last_update) < timedelta(seconds=10):
            return self.user_position
        return None

    def start_following(self):
        """Start follow-me mode"""
        self.follow_mode_active = True
        logger.info("Follow-me mode activated")

    def stop_following(self):
        """Stop follow-me mode"""
        self.follow_mode_active = False
        logger.info("Follow-me mode deactivated")

    def is_following(self) -> bool:
        """Check if follow mode is active"""
        return self.follow_mode_active

    def should_move_to_user(self, robot_x: int, robot_y: int) -> bool:
        """Check if robot should move to user's position

        Args:
            robot_x: Robot's current X position
            robot_y: Robot's current Y position

        Returns:
            True if robot should move
        """
        if not self.follow_mode_active:
            return False

        user_pos = self.get_position()
        if not user_pos:
            logger.warning("No recent user position, cannot follow")
            return False

        user_x, user_y = user_pos

        # Calculate distance
        distance = ((robot_x - user_x) ** 2 + (robot_y - user_y) ** 2) ** 0.5

        # Only move if user is far enough
        return distance > self.follow_distance

    async def follow_loop(self, valetudo_client):
        """Main follow loop - runs while follow mode is active

        Args:
            valetudo_client: ValetudoAPIClient instance
        """
        logger.info("Follow loop started")

        while self.follow_mode_active:
            try:
                user_pos = self.get_position()
                if not user_pos:
                    logger.warning("No user position, waiting...")
                    await asyncio.sleep(self.update_interval)
                    continue

                # Get robot position from map
                # Note: This is simplified - actual implementation would need to parse map data
                # For now, we'll just send goto command
                user_x, user_y = user_pos

                logger.info(f"Following user to position ({user_x}, {user_y})")
                await valetudo_client.goto_location(user_x, user_y)

                # Wait before next update
                await asyncio.sleep(self.update_interval)

            except Exception as e:
                logger.error(f"Error in follow loop: {e}")
                await asyncio.sleep(self.update_interval)

        logger.info("Follow loop stopped")


# Global tracker instance
user_tracker = UserTracker()
