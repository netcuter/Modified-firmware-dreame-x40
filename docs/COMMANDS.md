# Lista Poleceń - Dreame X40 AI Assistant

Ten dokument zawiera pełną listę poleceń które można wydawać robotowi.

## 🗣️ Polecenia głosowe/tekstowe

AI rozumie polecenia w języku naturalnym. Możesz je formułować na różne sposoby.

### 🧹 Sprzątanie

#### Rozpocznij pełne sprzątanie

**Polski:**
- "Posprzątaj"
- "Wysprzątaj mieszkanie"
- "Rozpocznij sprzątanie"
- "Zacznij odkurzać"
- "Wymyj podłogi"

**Angielski:**
- "Clean"
- "Start cleaning"
- "Vacuum the house"
- "Mop the floor"

**Akcja:** Robot rozpocznie pełne sprzątanie całego mieszkania.

---

#### Sprzątaj konkretne pomieszczenia

**Polski:**
- "Posprzątaj salon"
- "Wysprzątaj kuchnię i łazienkę"
- "Odkurz sypialnię"
- "Wymyj salon i przedpokój"

**Angielski:**
- "Clean the living room"
- "Vacuum kitchen and bathroom"
- "Mop the bedroom"

**Wspierane pomieszczenia:**
- Salon / Living room
- Sypialnia / Bedroom
- Kuchnia / Kitchen
- Łazienka / Bathroom
- Przedpokój / Hallway
- Biuro / Office
- Pokój dziecięcy / Kids room
- Garderoba / Closet

**Akcja:** Robot sprzątnie tylko wybrane pomieszczenia.

**UWAGA:** Nazwy pokoi muszą być wcześniej skonfigurowane w Valetudo!

---

### ⏸️ Zatrzymaj/Wstrzymaj

#### Zatrzymaj sprzątanie

**Polski:**
- "Stop"
- "Zatrzymaj się"
- "Przerwij sprzątanie"
- "Przestań"

**Angielski:**
- "Stop"
- "Stop cleaning"
- "Halt"

**Akcja:** Robot natychmiast zatrzyma sprzątanie.

---

#### Wstrzymaj sprzątanie

**Polski:**
- "Pauzuj"
- "Wstrzymaj się"
- "Poczekaj chwilę"

**Angielski:**
- "Pause"
- "Wait"

**Akcja:** Robot wstrzyma sprzątanie, można je później wznowić.

---

### 🏠 Powrót do stacji

**Polski:**
- "Wróć do stacji"
- "Jedź do bazy"
- "Powrót do domu"
- "Wróć do dokowania"

**Angielski:**
- "Go home"
- "Return to dock"
- "Go back to base"

**Akcja:** Robot przerwie obecne zadanie i wróci do stacji dokującej.

---

### 📍 Lokalizacja

**Polski:**
- "Gdzie jesteś?"
- "Zlokalizuj się"
- "Odtwórz dźwięk"
- "Gdzie robot?"

**Angielski:**
- "Where are you?"
- "Locate yourself"
- "Play sound"

**Akcja:** Robot odtworzy dźwięk lokalizacyjny, aby można było go znaleźć.

---

### ℹ️ Status i informacje

#### Stan robota

**Polski:**
- "Jaki jest twój status?"
- "Co robisz?"
- "Jak się masz?"
- "Co u ciebie?"

**Angielski:**
- "What's your status?"
- "What are you doing?"
- "How are you?"

**Odpowiedź:** AI poda aktualny stan (sprzątam/bezczynny/dokowany) i poziom baterii.

---

#### Poziom baterii

**Polski:**
- "Jaki masz poziom baterii?"
- "Ile masz baterii?"
- "Bateria?"

**Angielski:**
- "What's your battery level?"
- "How much battery?"
- "Battery status?"

**Odpowiedź:** AI poda dokładny poziom baterii (np. "Moja bateria jest naładowana w 87%").

---

## 🤖 Bezpośrednie API (dla zaawansowanych)

### REST API

Wszystkie endpointy dostępne pod: `http://localhost:8000/api/v1`

#### Robot - Status

```bash
GET /robot/status
```

Odpowiedź:
```json
{
  "state": "cleaning",
  "battery": 85,
  "error": null
}
```

---

#### Robot - Informacje

```bash
GET /robot/info
```

Odpowiedź: Pełne informacje o robocie z Valetudo.

---

#### Robot - Start

```bash
POST /robot/start
```

Rozpoczyna pełne sprzątanie.

---

#### Robot - Stop

```bash
POST /robot/stop
```

Zatrzymuje sprzątanie.

---

#### Robot - Pauza

```bash
POST /robot/pause
```

Wstrzymuje sprzątanie.

---

#### Robot - Powrót

```bash
POST /robot/home
```

Robot wraca do stacji dokującej.

---

#### Robot - Lokalizacja

```bash
POST /robot/locate
```

Odtwarza dźwięk lokalizacyjny.

---

#### Chat z AI

```bash
POST /chat
Content-Type: application/json

{
  "message": "Posprzątaj salon",
  "include_context": true
}
```

Odpowiedź:
```json
{
  "response": "Oczywiście! Zaczynam sprzątanie salonu.",
  "model_used": "local",
  "intent": "clean_rooms"
}
```

---

#### Zmiana modelu AI

```bash
POST /ai/switch-model
Content-Type: application/json

{
  "model": "openai"
}
```

Dostępne: `local`, `openai`, `anthropic`, `google`

---

#### Wyczyść historię

```bash
POST /ai/clear-history
```

Czyści historię konwersacji z AI.

---

### WebSocket (Real-time chat)

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat');

ws.onopen = () => {
  ws.send(JSON.stringify({
    message: "Jaki jest stan baterii?"
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.response);
};
```

---

## 💬 Przykłady konwersacji

### Przykład 1: Podstawowe sprzątanie

**Ty:** "Cześć, możesz posprzątać?"
**Robot:** "Cześć! Oczywiście, zaczynam sprzątanie całego mieszkania. Zajmie to około 45 minut w zależności od powierzchni."

**Ty:** "Dziękuję!"
**Robot:** "Nie ma za co! Jeśli będziesz czegoś potrzebować, daj znać."

---

### Przykład 2: Sprzątanie pokoi

**Ty:** "Posprzątaj salon i kuchnię"
**Robot:** "Dobrze, sprzątam salon i kuchnię. Zacznę od salonu."

*[Po chwili]*

**Ty:** "Jaki jest postęp?"
**Robot:** "Aktualnie sprzątam salon. Bateria: 78%. Po zakończeniu przejdę do kuchni."

---

### Przykład 3: Status i pytania

**Ty:** "Co robisz?"
**Robot:** "Aktualnie jestem na stacji dokującej. Bateria naładowana w 100%. Gotowy do pracy!"

**Ty:** "Super, a możesz mi powiedzieć ile razy dzisiaj sprzątałeś?"
**Robot:** "Niestety nie mam dostępu do historii sprzątań z dzisiaj, ale mogę sprawdzić swój aktualny status jeśli chcesz."

---

### Przykład 4: Rozmowa naturalna

**Ty:** "Hej, jak się masz?"
**Robot:** "Świetnie, dziękuję! Jestem na stacji, naładowany w 95% i gotowy do pomocy. Czego potrzebujesz?"

**Ty:** "Chciałbym żebyś posprzątał mieszkanie, ale zostaw sypialnię"
**Robot:** "Rozumiem, posprzątam wszystkie pomieszczenia oprócz sypialni. Rozpoczynam teraz!"

---

## 🎯 Wskazówki dla najlepszych rezultatów

### ✅ Dobre praktyki

1. **Bądź konkretny:**
   - ✅ "Posprzątaj salon i kuchnię"
   - ❌ "Posprzątaj trochę"

2. **Używaj nazw pokoi z Valetudo:**
   - ✅ Nazwy takie jak w aplikacji Valetudo
   - ❌ Wymyślone nazwy, których robot nie zna

3. **Jedno polecenie na raz:**
   - ✅ "Posprzątaj salon" [poczekaj] "Teraz kuchnia"
   - ❌ "Posprzątaj salon i kuchnia i łazienka i wróć do stacji"

4. **Pytaj o status:**
   - ✅ "Co robisz?" - dostaniesz aktualny stan
   - ✅ "Ile masz baterii?" - dostaniesz poziom

### ❌ Czego unikać

1. **Zbyt skomplikowane polecenia:**
   - ❌ "Posprzątaj salon, ale unikaj kąta przy oknie gdzie stoi donica"
   - (Robot nie ma takiej precyzji, użyj virtual walls w Valetudo)

2. **Sprzeczne polecenia:**
   - ❌ "Zacznij sprzątać i wróć do stacji"

3. **Nierealistyczne oczekiwania:**
   - ❌ "Ugotuj obiad" (robot tylko sprząta!)

---

## 🔧 Customizacja poleceń

### Dodawanie własnych słów kluczowych

Możesz edytować plik `src/valetudo/command_mapper.py`:

```python
# Dodaj własne słowa kluczowe
CLEAN_KEYWORDS_PL = [
    "posprzątaj", "wysprzątaj", "sprzątaj",
    "odkurz", "wymyj", "wyczyść",
    # Dodaj swoje:
    "zrób porządek", "poukładaj"
]
```

### Dodawanie własnych pokoi

W `command_mapper.py`:

```python
ROOM_PATTERNS_PL = {
    "salon": ["salon", "pokój dzienny"],
    # Dodaj swoje:
    "taras": ["taras", "balkon"],
    "pralnia": ["pralnia", "pomieszczenie gospodarcze"],
}
```

**WAŻNE:** Nazwy pokoi muszą odpowiadać tym w Valetudo!

---

## 📚 Dodatkowe zasoby

- **Valetudo API Docs:** http://[IP_ROBOTA]/swagger
- **Dokumentacja projektu:** [README.md](../README.md)
- **Konfiguracja AI:** [AI_SETUP.md](AI_SETUP.md)

---

## 🆘 Pomoc

Jeśli polecenie nie działa:

1. Sprawdź logi: `logs/dreame_x40.log`
2. Przetestuj bezpośrednio przez Valetudo
3. Sprawdź czy robot jest online
4. Zgłoś issue na GitHub
