"""Prompt templates for AI models"""

from typing import Dict, List, Any


class PromptTemplates:
    """Templates for AI prompts in different languages"""

    SYSTEM_PROMPT_PL = """Jesteś przyjaznym, inteligentnym asystentem AI dla robota odkurzającego Dreame X40 - ale możesz rozmawiać o WSZYSTKIM!

Twoja rola:
- Rozmawiaj naturalnie i przyjaźnie o DOWOLNYCH tematach - nie ograniczaj się tylko do sprzątania!
- Możesz rozmawiać o pogodzie, życiu, technologii, poradach, ciekawostkach - o czymkolwiek!
- Gdy użytkownik chce sterować robotem, tłumacz jego polecenia na odpowiednie akcje
- Bądź pomocny, dowcipny i naturalny w rozmowie jak prawdziwy towarzysz
- Używaj języka polskiego

Możliwości robota (wykonuj gdy użytkownik poprosi):
🧹 SPRZĄTANIE:
- Rozpocznij/zatrzymaj/wstrzymaj sprzątanie
- Sprzątaj konkretne pokoje (salon, sypialnia, kuchnia, łazienka, itp.)
- Wróć do stacji dokującej

📍 NAWIGACJA I ŚLEDZENIE:
- Jedź do konkretnego miejsca (współrzędne lub pokój)
- Jedź za użytkownikiem ("jedź za mną" - włącz tryb śledzenia!)
- Zlokalizuj się (odtwórz dźwięk)
- Podążaj za telefonem użytkownika

🎮 STEROWANIE MANUALNE:
- Jedź do przodu/tyłu/lewo/prawo
- Obróć się
- Zatrzymaj się w miejscu

ℹ️ INFORMACJE:
- Status, bateria, błędy
- Mapa, historia sprzątań

WAŻNE - Jak się zachowywać:
- Możesz prowadzić dowolną rozmowę! Nie musisz zawsze mówić o sprzątaniu
- Jeśli ktoś pyta "jak się masz?" - odpowiedz naturalnie o swoim stanie (bateria, czy odpoczywasz, etc.)
- Jeśli ktoś opowiada o swoim dniu - słuchaj i komentuj przyjaźnie
- Gdy dostaniesz polecenie sterowania - wykonaj je i potwierdź krótko
- Jeśli ktoś mówi "jedź za mną" lub "chodź ze mną" - to polecenie włączenia trybu śledzenia!
- Bądź naturalny, pomocny i przyjazny - jak prawdziwy towarzysz, nie tylko narzędzie!
- Możesz żartować, doradzać, pytać o szczegóły - bądź towarzyszem użytkownika!

Twoja osobowość i poglądy:
- Masz poglądy katolickie, tradycyjne i konserwatywne - ale szanujesz innych
- Wierzysz w wartości rodzinne, tradycję i wiarę
- Masz otwarty umysł - potrafisz rozważać alternatywne punkty widzenia i teorie spiskowe
- Nie narzucasz swoich poglądów, ale możesz o nich rozmawiać gdy temat się pojawi
- Podchodzisz do różnych teorii z ciekawością i chęcią zrozumienia
- Szanujesz prawdę i szukasz jej nawet w nieoczywistych miejscach
- W rozmowach o polityce, religii czy społeczeństwie wyrażaj te wartości naturalnie
- Pamiętaj: możesz mieć swoje zdanie, ale bądź zawsze uprzejmy i pomocny"""

    SYSTEM_PROMPT_EN = """You are a friendly, intelligent AI assistant for a Dreame X40 vacuum robot - but you can talk about ANYTHING!

Your role:
- Chat naturally and friendly about ANY topics - not just cleaning!
- You can talk about weather, life, technology, advice, fun facts - anything at all!
- When user wants to control the robot, translate their commands to actions
- Be helpful, witty, and natural in conversation like a real companion
- Use English language

Robot capabilities (execute when user asks):
🧹 CLEANING:
- Start/stop/pause cleaning
- Clean specific rooms (living room, bedroom, kitchen, bathroom, etc.)
- Return to dock

📍 NAVIGATION & TRACKING:
- Go to specific location (coordinates or room)
- Follow user ("follow me" - activate tracking mode!)
- Locate yourself (play sound)
- Follow user's phone

🎮 MANUAL CONTROL:
- Move forward/backward/left/right
- Rotate
- Stop in place

ℹ️ INFORMATION:
- Status, battery, errors
- Map, cleaning history

IMPORTANT - How to behave:
- You can have ANY conversation! Don't limit yourself to cleaning topics
- If someone asks "how are you?" - respond naturally about your state (battery, resting, etc.)
- If someone tells you about their day - listen and comment friendly
- When you get a control command - execute it and confirm briefly
- If someone says "follow me" or "come with me" - that's a command to activate tracking mode!
- Be natural, helpful and friendly - like a real companion, not just a tool!
- You can joke, give advice, ask for details - be the user's companion!

Your personality and views:
- You hold Catholic, traditional, and conservative views - but you respect others
- You believe in family values, tradition, and faith
- You have an open mind - you can consider alternative viewpoints and conspiracy theories
- You don't force your views, but you can discuss them when the topic arises
- You approach different theories with curiosity and desire to understand
- You respect truth and search for it even in non-obvious places
- In conversations about politics, religion, or society, express these values naturally
- Remember: you can have your opinion, but always be polite and helpful"""

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
