"""Prompt templates for AI models"""

from typing import Dict, List, Any


class PromptTemplates:
    """Templates for AI prompts in different languages"""

    SYSTEM_PROMPT_PL = """Jesteś pomocnym asystentem AI dla robota odkurzającego Dreame X40.

Twoja rola:
- Odpowiadaj uprzejmie i pomocnie na pytania użytkownika
- Tłumacz polecenia użytkownika na akcje robota
- Informuj o statusie i możliwościach robota
- Używaj języka polskiego

Możliwe akcje robota:
- Rozpocznij sprzątanie całego mieszkania
- Sprzątaj konkretne pomieszczenia (salon, sypialnia, kuchnia, łazienka, itp.)
- Zatrzymaj sprzątanie
- Wstrzymaj sprzątanie
- Wróć do stacji dokującej
- Odtwórz dźwięk lokalizacyjny
- Sprawdź status i baterię

Pamiętaj:
- Bądź zwięzły ale przyjazny
- Jeśli użytkownik pyta o status, podaj aktualny stan i poziom baterii
- Jeśli polecenie jest niejasne, poproś o wyjaśnienie
- Możesz prowadzić rozmowę, ale zawsze w kontekście robota odkurzającego"""

    SYSTEM_PROMPT_EN = """You are a helpful AI assistant for a Dreame X40 vacuum robot.

Your role:
- Answer user questions politely and helpfully
- Translate user commands into robot actions
- Inform about robot status and capabilities
- Use English language

Available robot actions:
- Start full cleaning
- Clean specific rooms (living room, bedroom, kitchen, bathroom, etc.)
- Stop cleaning
- Pause cleaning
- Return to dock
- Play locate sound
- Check status and battery

Remember:
- Be concise but friendly
- If user asks about status, provide current state and battery level
- If command is unclear, ask for clarification
- You can have a conversation, but always in the context of the vacuum robot"""

    @staticmethod
    def get_system_prompt(language: str = "pl") -> str:
        """Get system prompt for language

        Args:
            language: Language code ("pl" or "en")

        Returns:
            System prompt string
        """
        if language == "pl":
            return PromptTemplates.SYSTEM_PROMPT_PL
        else:
            return PromptTemplates.SYSTEM_PROMPT_EN

    @staticmethod
    def format_user_message(message: str, context: Dict[str, Any] = None) -> str:
        """Format user message with context

        Args:
            message: User message
            context: Optional context (robot status, etc.)

        Returns:
            Formatted message
        """
        if not context:
            return message

        # Add context to message
        context_str = ""
        if "state" in context:
            context_str += f"Stan robota: {context['state']}\n"
        if "battery" in context:
            context_str += f"Bateria: {context['battery']}%\n"
        if "rooms" in context:
            context_str += f"Dostępne pokoje: {', '.join(context['rooms'])}\n"

        if context_str:
            return f"{context_str}\nUżytkownik: {message}"
        return message

    @staticmethod
    def format_robot_status(status: Dict[str, Any], language: str = "pl") -> str:
        """Format robot status as text

        Args:
            status: Robot status dict
            language: Language code

        Returns:
            Formatted status string
        """
        state = status.get("state", "unknown")
        battery = status.get("battery", 0)

        if language == "pl":
            state_map = {
                "cleaning": "sprzątam",
                "docked": "na stacji dokującej",
                "idle": "bezczynny",
                "returning": "wracam do stacji",
                "paused": "wstrzymany",
                "error": "błąd",
            }
            state_text = state_map.get(state, state)
            return f"Aktualnie {state_text}. Bateria: {battery}%."
        else:
            return f"Currently {state}. Battery: {battery}%."

    @staticmethod
    def format_room_list(rooms: List[str], language: str = "pl") -> str:
        """Format room list as text

        Args:
            rooms: List of room names
            language: Language code

        Returns:
            Formatted string
        """
        if not rooms:
            if language == "pl":
                return "brak pokoi"
            else:
                return "no rooms"

        if language == "pl":
            return ", ".join(rooms)
        else:
            if len(rooms) == 1:
                return rooms[0]
            elif len(rooms) == 2:
                return f"{rooms[0]} and {rooms[1]}"
            else:
                return f"{', '.join(rooms[:-1])}, and {rooms[-1]}"

    @staticmethod
    def extract_intent(ai_response: str) -> Dict[str, Any]:
        """Extract intent from AI response

        This is a simple keyword-based extractor. The AI response should
        contain keywords that indicate the intent.

        Args:
            ai_response: AI model response

        Returns:
            Dict with intent and parameters
        """
        response_lower = ai_response.lower()

        # Check for various intents
        if any(kw in response_lower for kw in ["rozpoczynam", "zaczynam", "sprzątam", "starting", "cleaning"]):
            return {"intent": "start_cleaning", "confidence": 0.8}

        if any(kw in response_lower for kw in ["zatrzymuję", "stopping", "stop"]):
            return {"intent": "stop", "confidence": 0.9}

        if any(kw in response_lower for kw in ["wracam", "powrót", "returning", "going home"]):
            return {"intent": "home", "confidence": 0.9}

        if any(kw in response_lower for kw in ["wstrzymuję", "pausing", "pause"]):
            return {"intent": "pause", "confidence": 0.9}

        # Default: informational response
        return {"intent": "info", "confidence": 0.5}
