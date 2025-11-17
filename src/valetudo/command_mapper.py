"""Command Mapper - Maps natural language to Valetudo commands"""

import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Command:
    """Parsed command"""
    action: str
    params: Dict[str, Any]
    confidence: float = 1.0


class CommandMapper:
    """Maps natural language commands to Valetudo API calls"""

    # Polish keywords for actions
    CLEAN_KEYWORDS_PL = [
        "posprzątaj", "wysprzątaj", "sprzątaj", "odkurz", "wymyj", "wyczyść"
    ]
    STOP_KEYWORDS_PL = [
        "stop", "zatrzymaj", "przerwij", "przestań"
    ]
    PAUSE_KEYWORDS_PL = [
        "pauzuj", "wstrzymaj", "poczekaj"
    ]
    HOME_KEYWORDS_PL = [
        "wróć", "powrót", "dom", "stacja", "baza", "dokuj"
    ]
    LOCATE_KEYWORDS_PL = [
        "gdzie jesteś", "znajdź się", "lokalizuj", "dźwięk"
    ]
    STATUS_KEYWORDS_PL = [
        "status", "stan", "jak się masz", "co robisz", "bateria"
    ]
    FOLLOW_KEYWORDS_PL = [
        "jedź za mną", "chodź za mną", "podążaj za mną", "śledź mnie",
        "chodź ze mną", "jedź ze mną", "follow me"
    ]
    GOTO_KEYWORDS_PL = [
        "jedź do", "pojed do", "idź do", "przejed do"
    ]
    MOVE_KEYWORDS_PL = {
        "forward": ["jedź do przodu", "do przodu", "naprzód"],
        "backward": ["jedź do tyłu", "do tyłu", "cofnij się"],
        "left": ["w lewo", "skręć w lewo", "obróć się w lewo"],
        "right": ["w prawo", "skręć w prawo", "obróć się w prawo"]
    }

    # English keywords
    CLEAN_KEYWORDS_EN = [
        "clean", "vacuum", "mop", "start"
    ]
    STOP_KEYWORDS_EN = [
        "stop", "halt", "cancel"
    ]
    PAUSE_KEYWORDS_EN = [
        "pause", "wait"
    ]
    HOME_KEYWORDS_EN = [
        "home", "dock", "return", "base"
    ]
    LOCATE_KEYWORDS_EN = [
        "where are you", "locate", "find", "sound"
    ]
    STATUS_KEYWORDS_EN = [
        "status", "state", "battery", "how are you"
    ]
    FOLLOW_KEYWORDS_EN = [
        "follow me", "come with me", "track me", "follow along"
    ]
    GOTO_KEYWORDS_EN = [
        "go to", "move to", "navigate to", "head to"
    ]
    MOVE_KEYWORDS_EN = {
        "forward": ["move forward", "go forward", "ahead"],
        "backward": ["move backward", "go back", "reverse"],
        "left": ["turn left", "go left", "rotate left"],
        "right": ["turn right", "go right", "rotate right"]
    }

    # Room names mapping (Polish -> common patterns)
    ROOM_PATTERNS_PL = {
        "salon": ["salon", "pokój dzienny"],
        "sypialnia": ["sypialnia", "sypialnia"],
        "kuchnia": ["kuchnia", "kuchni"],
        "łazienka": ["łazienka", "łazience"],
        "przedpokój": ["przedpokój", "korytarz", "hol"],
        "biuro": ["biuro", "gabinet"],
        "dziecięcy": ["pokój dziecięcy", "dziecięcy", "dziecka"],
        "garderoba": ["garderoba", "szafa"],
    }

    # Room names mapping (English -> common patterns)
    ROOM_PATTERNS_EN = {
        "living room": ["living room", "lounge"],
        "bedroom": ["bedroom", "bed room"],
        "kitchen": ["kitchen"],
        "bathroom": ["bathroom", "bath"],
        "hallway": ["hallway", "corridor", "hall"],
        "office": ["office", "study"],
        "kids room": ["kids room", "children's room", "child's room"],
        "closet": ["closet", "wardrobe"],
    }

    def __init__(self, language: str = "pl"):
        """Initialize command mapper

        Args:
            language: Default language ("pl" or "en")
        """
        self.language = language
        logger.info(f"Initialized CommandMapper with language: {language}")

    def detect_language(self, text: str) -> str:
        """Detect language of text

        Args:
            text: Input text

        Returns:
            Language code ("pl" or "en")
        """
        text_lower = text.lower()

        # Polish-specific characters
        pl_chars = ["ą", "ć", "ę", "ł", "ń", "ó", "ś", "ź", "ż"]
        has_pl_chars = any(char in text_lower for char in pl_chars)

        # Polish keywords
        pl_keywords = ["posprzątaj", "wróć", "gdzie", "jest", "bateria"]
        has_pl_keywords = any(kw in text_lower for kw in pl_keywords)

        if has_pl_chars or has_pl_keywords:
            return "pl"
        return "en"

    def parse_command(self, text: str) -> Optional[Command]:
        """Parse natural language command

        Args:
            text: Natural language command

        Returns:
            Parsed Command object or None if not recognized
        """
        text_lower = text.lower()
        lang = self.detect_language(text)

        logger.debug(f"Parsing command (lang={lang}): {text}")

        # Select keywords based on detected language
        if lang == "pl":
            clean_kw = self.CLEAN_KEYWORDS_PL
            stop_kw = self.STOP_KEYWORDS_PL
            pause_kw = self.PAUSE_KEYWORDS_PL
            home_kw = self.HOME_KEYWORDS_PL
            locate_kw = self.LOCATE_KEYWORDS_PL
            status_kw = self.STATUS_KEYWORDS_PL
            follow_kw = self.FOLLOW_KEYWORDS_PL
            goto_kw = self.GOTO_KEYWORDS_PL
            move_kw = self.MOVE_KEYWORDS_PL
            room_patterns = self.ROOM_PATTERNS_PL
        else:
            clean_kw = self.CLEAN_KEYWORDS_EN
            stop_kw = self.STOP_KEYWORDS_EN
            pause_kw = self.PAUSE_KEYWORDS_EN
            home_kw = self.HOME_KEYWORDS_EN
            locate_kw = self.LOCATE_KEYWORDS_EN
            status_kw = self.STATUS_KEYWORDS_EN
            follow_kw = self.FOLLOW_KEYWORDS_EN
            goto_kw = self.GOTO_KEYWORDS_EN
            move_kw = self.MOVE_KEYWORDS_EN
            room_patterns = self.ROOM_PATTERNS_EN

        # Check for cleaning commands
        if any(kw in text_lower for kw in clean_kw):
            rooms = self._extract_rooms(text_lower, room_patterns)
            if rooms:
                return Command(
                    action="clean_rooms",
                    params={"rooms": rooms},
                    confidence=0.9
                )
            else:
                return Command(
                    action="start_cleaning",
                    params={},
                    confidence=0.95
                )

        # Check for stop commands
        if any(kw in text_lower for kw in stop_kw):
            return Command(action="stop", params={}, confidence=0.95)

        # Check for pause commands
        if any(kw in text_lower for kw in pause_kw):
            return Command(action="pause", params={}, confidence=0.95)

        # Check for home/dock commands
        if any(kw in text_lower for kw in home_kw):
            return Command(action="home", params={}, confidence=0.95)

        # Check for locate commands
        if any(kw in text_lower for kw in locate_kw):
            return Command(action="locate", params={}, confidence=0.9)

        # Check for status commands
        if any(kw in text_lower for kw in status_kw):
            return Command(action="status", params={}, confidence=0.9)

        # Check for follow me commands
        if any(kw in text_lower for kw in follow_kw):
            return Command(action="follow_me", params={}, confidence=0.95)

        # Check for goto commands
        if any(kw in text_lower for kw in goto_kw):
            # Try to extract room/location
            rooms = self._extract_rooms(text_lower, room_patterns)
            if rooms:
                return Command(
                    action="goto_room",
                    params={"room": rooms[0]},
                    confidence=0.9
                )
            else:
                return Command(
                    action="goto_location",
                    params={},
                    confidence=0.7
                )

        # Check for manual movement commands
        for direction, keywords in move_kw.items():
            if any(kw in text_lower for kw in keywords):
                return Command(
                    action="move",
                    params={"direction": direction},
                    confidence=0.9
                )

        logger.warning(f"Could not parse command: {text}")
        return None

    def _extract_rooms(self, text: str, room_patterns: Dict[str, List[str]]) -> List[str]:
        """Extract room names from text

        Args:
            text: Input text (lowercase)
            room_patterns: Room name patterns for current language

        Returns:
            List of room identifiers
        """
        rooms = []
        for room_id, patterns in room_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    rooms.append(room_id)
                    break

        logger.debug(f"Extracted rooms: {rooms}")
        return rooms

    def command_to_api_call(self, command: Command) -> Tuple[str, str, Optional[Dict[str, Any]]]:
        """Convert Command to Valetudo API call

        Args:
            command: Parsed Command object

        Returns:
            Tuple of (method, endpoint, data)
            method: "GET" or "PUT"
            endpoint: API endpoint
            data: JSON data for PUT requests (or None for GET)
        """
        action = command.action
        params = command.params

        # Map actions to API calls
        if action == "start_cleaning":
            return ("PUT", "robot/capabilities/BasicControlCapability", {"action": "start"})

        elif action == "stop":
            return ("PUT", "robot/capabilities/BasicControlCapability", {"action": "stop"})

        elif action == "pause":
            return ("PUT", "robot/capabilities/BasicControlCapability", {"action": "pause"})

        elif action == "home":
            return ("PUT", "robot/capabilities/BasicControlCapability", {"action": "home"})

        elif action == "locate":
            return ("PUT", "robot/capabilities/LocateCapability", {"action": "locate"})

        elif action == "status":
            return ("GET", "robot/state", None)

        elif action == "clean_rooms":
            # Note: This requires segment IDs, which need to be mapped from room names
            # For now, we return the room names and let the caller handle the mapping
            return ("CLEAN_ROOMS", "robot/capabilities/MapSegmentationCapability", {
                "room_names": params.get("rooms", [])
            })

        else:
            logger.warning(f"Unknown action: {action}")
            return ("GET", "robot/state", None)

    def get_response_template(self, command: Command, lang: str = None) -> str:
        """Get response template for command

        Args:
            command: Parsed Command object
            lang: Language code (defaults to instance language)

        Returns:
            Response template string
        """
        if lang is None:
            lang = self.language

        action = command.action

        if lang == "pl":
            templates = {
                "start_cleaning": "Oczywiście! Zaczynam sprzątanie całego mieszkania.",
                "clean_rooms": "Dobrze, sprzątam: {rooms}.",
                "stop": "Zatrzymuję sprzątanie.",
                "pause": "Wstrzymuję sprzątanie.",
                "home": "Wracam do stacji dokującej.",
                "locate": "Odtwarzam dźwięk lokalizacyjny.",
                "status": "Aktualnie {state}. Bateria: {battery}%.",
            }
        else:
            templates = {
                "start_cleaning": "Sure! Starting full cleaning.",
                "clean_rooms": "Okay, cleaning: {rooms}.",
                "stop": "Stopping cleaning.",
                "pause": "Pausing cleaning.",
                "home": "Returning to dock.",
                "locate": "Playing locate sound.",
                "status": "Currently {state}. Battery: {battery}%.",
            }

        return templates.get(action, "")
