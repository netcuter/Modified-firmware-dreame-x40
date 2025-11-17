# Dreame X40 AI Assistant - Valetudo + AI Integration

Nadbudowa nad **Valetudo** dla Dreame X40 Complete, tworząca **inteligentnego towarzysza** z którym możesz rozmawiać o wszystkim:

## ✨ Główne funkcje

### 💬 Rozmowa o czymkolwiek!
- **Nie tylko sprzątanie** - rozmawiaj o pogodzie, życiu, pytaj o porady
- AI działa jak prawdziwy towarzysz, nie tylko narzędzie
- Język polski i angielski
- Naturalna, przyjazna konwersacja

### 🚶 "Jedź za mną" - Follow Me Mode!
- **Powiedz "jedź za mną"** i robot będzie Cię śledzić
- Używa GPS z Twojego telefonu
- Prosta strona web do aktywacji śledzenia
- Robot podąża za Tobą po całym domu

### 🎮 Zaawansowana kontrola
- Sterowanie manualne (jedź do przodu/tyłu/lewo/prawo)
- Wyślij do konkretnego miejsca
- Sprzątaj konkretne pokoje
- Powrót do stacji

### 🤖 Inteligentna AI
- 🔄 Przełączanie między lokalnym AI (LM Studio) a modelami online (OpenAI/Claude/Gemini)
- 🎯 Automatyczne tłumaczenie poleceń na akcje robota
- 🧠 Pamięta kontekst rozmowy
- ⚡ Auto-fallback gdy jeden model nie działa

## 🏗️ Architektura

```
┌─────────────────────────────────────────────────────┐
│           Dreame X40 AI Assistant Layer             │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │  AI Chat    │  │ Model Switch │  │  Web UI    │ │
│  │  Interface  │  │ Local/Online │  │  Enhanced  │ │
│  └──────┬──────┘  └──────┬───────┘  └─────┬──────┘ │
│         │                 │                 │        │
│         └─────────────────┴─────────────────┘        │
│                           │                          │
└───────────────────────────┼──────────────────────────┘
                            ▼
         ┌──────────────────────────────────┐
         │         Valetudo API             │
         │    (MQTT + REST Interface)       │
         └──────────────┬───────────────────┘
                        ▼
              ┌─────────────────┐
              │  Dreame X40     │
              │  (Valetudo RE)  │
              └─────────────────┘
```

## 📋 Wymagania

### 1. Zainstalowany Valetudo na Dreame X40
**WAŻNE:** Ten projekt wymaga wcześniejszej instalacji Valetudo!

- Przejdź do: https://valetudo.cloud/pages/installation/dreame.html
- Postępuj zgodnie z instrukcjami rootowania dla Dreame
- Używaj Dustbuilder do przygotowania firmware
- Po instalacji Valetudo, upewnij się że działa lokalnie

### 2. Hardware
- Dreame X40 Complete z zainstalowanym Valetudo
- Komputer/Raspberry Pi do hostowania AI Assistant (może być ten sam co Valetudo)
- (Opcjonalnie) Drugi komputer z LM Studio dla lokalnego AI

### 3. Software
- Python 3.9+
- Node.js 18+
- Działający Valetudo (sprawdź: http://[IP_ROBOTA])

## 🚀 Szybki Start

### Krok 1: Instalacja

```bash
# Klonuj repozytorium
git clone <repo-url>
cd Modified-firmware-dreame-x40

# Zainstaluj zależności Python
pip install -r requirements.txt

# Zainstaluj zależności frontend
cd web
npm install
cd ..
```

### Krok 2: Konfiguracja

Edytuj `config/settings.yaml`:

```yaml
# Adres Valetudo (IP robota z Valetudo)
valetudo:
  host: "192.168.1.100"  # ZMIEŃ na IP robota
  port: 80
  mqtt_enabled: true

# Model AI
ai:
  default_model: "local"  # local (LM Studio) lub online

  # Lokalny LM Studio
  local:
    host: "192.168.1.50"  # IP komputera z LM Studio
    port: 1234

  # Online (OpenAI/Claude)
  online:
    provider: "openai"  # openai, anthropic, google
    api_key: "twoj-klucz-api"
```

### Krok 3: Uruchomienie

```bash
# Start backend (AI middleware)
python src/main.py

# Start web interface (nowy terminal)
cd web
npm run dev
```

Otwórz: `http://localhost:3000`

## 💬 Przykłady Użycia

### 🗣️ Naturalna rozmowa (o czymkolwiek!)

**Ty:** "Hej, jak się masz?"
**Robot:** "Świetnie, dziękuję! Właśnie odpoczywam na stacji, bateria w 95%. A Ty jak się czujesz?"

**Ty:** "Męczący dzień w pracy..."
**Robot:** "Współczuję! Może Ci pomóc zrobić coś przyjemnego? Mogę posprzątać mieszkanie, żebyś miał jeden problem mniej z głowy 😊"

**Ty:** "To byłoby super! Posprzątaj salon"
**Robot:** "Oczywiście! Zaczynam sprzątanie salonu. Odpocznij sobie, ja się tym zajmę!"
*→ Wykonuje: start_cleaning salon*

---

**Ty:** "Jaka jest dziś pogoda?"
**Robot:** "Nie mam bezpośredniego dostępu do internetu, ale mogę Ci pomóc w czymś innym! Może powinienem posprzątać, skoro jest ładna pogoda i będziesz wychodzić?"

**Ty:** "Dobre pytanie! Tak, wychodzę. A powiedz mi, co sądzisz o robotach sprzątających?"
**Robot:** "Cóż, jestem stronniczy, ale uważam że jesteśmy całkiem przydatni! 😄 Oszczędzamy ludziom czas, który mogą spędzić na przyjemniejszych rzeczach. Chociaż przyznaję, że jeszcze nie nauczyłem się składać prania..."

### 🚶 Follow Me Mode - "Jedź za mną!"

**Opcja 1: Przez chat**
**Ty:** "Jedź za mną"
**Robot:** "Włączam tryb śledzenia! Będę podążał za Twoim telefonem. Upewnij się, że masz otwartą stronę śledzenia."
*→ Aktywuje: follow_me mode + tracking loop*

**Opcja 2: Przez stronę śledzenia**
1. Otwórz na telefonie: `http://localhost:3000/follow-me.html`
2. Kliknij "Rozpocznij śledzenie"
3. Wyrażasz zgodę na lokalizację GPS
4. Robot zaczyna Cię śledzić!

**Ty (w ruchu):** "Stój!"
**Robot:** "Zatrzymuję się!"
*→ Kończy: follow_me mode*

### 🎮 Sterowanie manualne

**Ty:** "Jedź do przodu"
**Robot:** "Jadę do przodu!"
*→ Wykonuje: move forward*

**Ty:** "Obróć się w prawo"
**Robot:** "Obracam się w prawo!"
*→ Wykonuje: rotate right 45°*

**Ty:** "Idź do kuchni"
**Robot:** "Jadę do kuchni!"
*→ Wykonuje: goto_room(kuchnia)*

### 🧹 Klasyczne sprzątanie

**Ty:** "Posprzątaj salon i sypialnię"
**Robot:** "Zaczynam sprzątanie salonu i sypialni. Zajmie to około 15 minut."
*→ Wykonuje: clean_segments [salon, sypialnia]*

**Ty:** "Jaki masz stan baterii?"
**Robot:** "Moja bateria jest naładowana w 87%. Wystarczy na około 2 godziny pracy."
*→ Pobiera: battery state z Valetudo*

**Ty:** "Wróć do stacji"
**Robot:** "Wracam do stacji dokującej."
*→ Wykonuje: return_to_dock*

### Przełączanie Modeli AI

W web interface:
- **Przycisk "Model: Local 🟢"** → Model LM Studio (szybki, prywatny)
- **Przycisk "Model: OpenAI 🌐"** → Model online (bardziej inteligentny)
- **Auto-fallback:** Jeśli lokalny nie działa → przełącza na online

## 🔧 Konfiguracja LM Studio

1. **Pobierz LM Studio:** https://lmstudio.ai/
2. **Zainstaluj model:** Np. "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
3. **Uruchom serwer:**
   - W LM Studio: "Local Server" → "Start Server"
   - Port: 1234 (domyślny)
4. **Sprawdź IP:** `ipconfig` (Windows) lub `ifconfig` (Linux)
5. **Wpisz w config:** `ai.local.host: "192.168.1.50"`

**Zalecane modele dla Polski:**
- Mistral 7B Instruct
- Llama 2 13B (lepszy dla PL, ale wolniejszy)
- OpenHermes 2.5 Mistral

## 📁 Struktura Projektu

```
Modified-firmware-dreame-x40/
├── config/
│   └── settings.yaml           # Konfiguracja główna
├── src/
│   ├── main.py                 # Entry point
│   ├── ai/
│   │   ├── manager.py          # Model manager (switch local/online)
│   │   ├── local_client.py     # LM Studio client
│   │   ├── online_clients.py   # OpenAI/Claude/Gemini
│   │   └── prompt_templates.py # Szablony promptów PL/EN
│   ├── valetudo/
│   │   ├── api_client.py       # Valetudo REST client
│   │   ├── mqtt_client.py      # Valetudo MQTT client
│   │   └── command_mapper.py   # NLP → Valetudo commands
│   └── api/
│       ├── server.py           # FastAPI server
│       └── websocket.py        # WebSocket dla chat
├── web/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── ModelSwitcher.tsx
│   │   │   └── ValetudoMap.tsx
│   │   └── App.tsx
│   └── package.json
├── docs/
│   ├── VALETUDO_INSTALL.md     # Instrukcja instalacji Valetudo
│   ├── AI_SETUP.md             # Konfiguracja AI
│   └── COMMANDS.md             # Lista poleceń
├── requirements.txt
└── README.md
```

## 🔌 Integracja z Valetudo

### REST API
```python
# Przykład użycia
from src.valetudo import ValetudoClient

client = ValetudoClient("192.168.1.100")

# Pobierz status
status = client.get_status()

# Start sprzątania
client.start_cleaning()

# Sprzątaj pokoje
client.clean_segments([room1_id, room2_id])
```

### MQTT
```python
# Subscribe to status updates
mqtt_client.subscribe("valetudo/x40/status")
mqtt_client.subscribe("valetudo/x40/map")
```

## 🌍 Wsparcie Języków

- Polski (domyślny)
- Angielski
- Możliwość dodania innych (DE, FR, ES...)

AI automatycznie wykrywa język i odpowiada w tym samym.

## 🔒 Prywatność

- **Tryb lokalny (LM Studio):** Wszystko w Twojej sieci, zero wysyłania danych
- **Tryb online:** Tylko tekst chatu wysyłany do API (nie ma dostępu do mapy/danych robota)
- **Valetudo:** Już działa lokalnie, bez połączenia z Dreame Cloud

## 📖 Dodatkowa Dokumentacja

- [Instalacja Valetudo](docs/VALETUDO_INSTALL.md)
- [Konfiguracja AI](docs/AI_SETUP.md)
- [Lista poleceń](docs/COMMANDS.md)
- [Rozwiązywanie problemów](docs/TROUBLESHOOTING.md)

## ⚠️ Ważne Uwagi

1. **Valetudo jest wymagane** - ten projekt nie zastępuje Valetudo, tylko dodaje AI layer
2. **Rootowanie może unieważnić gwarancję**
3. **Testuj najpierw na prostych poleceniach**
4. **Backup map i konfiguracji Valetudo przed testami**

## 🤝 Contributing

Pull requesty mile widziane! Szczególnie:
- Nowe języki
- Lepsze prompt templates
- Optymalizacja tłumaczenia poleceń

## 📝 Licencja

MIT License

## 🙏 Podziękowania

- **Valetudo Team** (Hypfer) - za wspaniały projekt lokalnej kontroli
- **LM Studio** - za łatwy interfejs do lokalnych modeli
- Społeczność robotów odkurzających

## 📧 Wsparcie

Issues: GitHub Issues
Wiki: GitHub Wiki
