# Rozwiązywanie Problemów

Ten dokument pomaga w rozwiązywaniu najczęstszych problemów z Dreame X40 AI Assistant.

## 🔍 Diagnostyka

### Sprawdź logi

```bash
# Logi backendu
tail -f logs/dreame_x40.log

# Logi w czasie rzeczywistym
python src/main.py
```

### Sprawdź health check

```bash
curl http://localhost:8000/api/v1/health
```

Odpowiedź powinna zawierać:
```json
{
  "status": "healthy",
  "valetudo": "connected",
  "ai": "available",
  "available_models": ["local", "openai"]
}
```

## 🤖 Problemy z Valetudo

### "Failed to connect to Valetudo"

**Objawy:**
- Błąd połączenia w logach
- Status: `valetudo: "disconnected"`
- Brak danych o robocie

**Rozwiązania:**

1. **Sprawdź IP robota:**
   ```bash
   ping 192.168.1.100  # Twoje IP robota
   ```

2. **Sprawdź czy Valetudo działa:**
   ```bash
   curl http://192.168.1.100
   ```
   Powinieneś zobaczyć interfejs Valetudo.

3. **Sprawdź konfigurację:**
   ```yaml
   # config/settings.yaml
   valetudo:
     host: "192.168.1.100"  # Poprawny IP?
     port: 80                # Poprawny port?
     protocol: "http"        # http czy https?
   ```

4. **Sprawdź firewall:**
   - Na robocie
   - Na komputerze z backendem

---

### "Timeout when calling Valetudo API"

**Przyczyny:**
- Sieć wolna
- Robot przeciążony
- Valetudo nie odpowiada

**Rozwiązania:**

1. Zwiększ timeout:
   ```yaml
   valetudo:
     timeout: 30  # Zwiększ do 30 sekund
   ```

2. Zrestartuj Valetudo:
   ```bash
   ssh root@192.168.1.100
   initctl restart valetudo
   ```

3. Zrestartuj robota (fizyczny przycisk power)

---

## 🧠 Problemy z AI

### "Local AI client not responding"

**Objawy:**
- Nie można użyć modelu lokalnego
- Auto-fallback na model online
- Timeout przy próbie połączenia

**Rozwiązania:**

1. **Sprawdź czy LM Studio działa:**
   ```bash
   curl http://192.168.1.50:1234/v1/models
   ```

2. **Sprawdź IP i port:**
   ```yaml
   ai:
     local:
       host: "192.168.1.50"  # Poprawny IP komputera?
       port: 1234             # LM Studio używa 1234
   ```

3. **Sprawdź czy server jest uruchomiony w LM Studio:**
   - Otwórz LM Studio
   - Zakładka "Local Server"
   - Kliknij "Start Server"

4. **Sprawdź firewall:**
   ```bash
   # Windows
   netsh advfirewall firewall add rule name="LM Studio" dir=in action=allow protocol=TCP localport=1234

   # Linux (ufw)
   sudo ufw allow 1234/tcp
   ```

5. **Test bezpośrednio:**
   ```bash
   curl -X POST http://192.168.1.50:1234/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model":"local-model","messages":[{"role":"user","content":"Hi"}]}'
   ```

---

### "OpenAI request failed: Incorrect API key"

**Rozwiązania:**

1. **Sprawdź klucz API:**
   - Zaloguj się na https://platform.openai.com/api-keys
   - Sprawdź czy klucz jest aktywny
   - Skopiuj ponownie (klucze są pokazywane tylko raz!)

2. **Sprawdź format klucza:**
   - Powinien zaczynać się od `sk-`
   - Długość ~50-60 znaków
   - Bez spacji na początku/końcu

3. **Zaktualizuj konfigurację:**
   ```yaml
   ai:
     online:
       openai:
         api_key: "sk-xxxxxxxxxxxxxxxxxxxxxxxx"  # Nowy klucz
   ```

4. **Użyj .env (zalecane):**
   ```bash
   # .env
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

### "Rate limit exceeded"

**Objawy:**
- Błąd 429 z OpenAI/Anthropic
- "Too many requests"

**Rozwiązania:**

1. **Poczekaj chwilę** (rate limity się resetują)

2. **Sprawdź limity konta:**
   - OpenAI: https://platform.openai.com/account/limits
   - Anthropic: https://console.anthropic.com/settings/limits

3. **Zmień model:**
   ```yaml
   ai:
     online:
       openai:
         model: "gpt-3.5-turbo"  # Tańszy, wyższe limity
   ```

4. **Użyj lokalnego modelu jako domyślnego**

---

## 🌐 Problemy z Web Interface

### "Cannot connect to backend"

**Objawy:**
- Strona się ładuje, ale brak danych
- Błędy w konsoli przeglądarki

**Rozwiązania:**

1. **Sprawdź czy backend działa:**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

2. **Sprawdź proxy w vite.config.ts:**
   ```typescript
   server: {
     proxy: {
       '/api': {
         target: 'http://localhost:8000',  // Poprawny?
       }
     }
   }
   ```

3. **Sprawdź CORS:**
   ```yaml
   api:
     cors_origins:
       - "http://localhost:3000"  # Dodaj frontend URL
   ```

4. **Sprawdź logi przeglądarki:**
   - F12 → Console
   - Szukaj błędów CORS lub network errors

---

### "Model switcher not working"

**Rozwiązania:**

1. **Sprawdź dostępne modele:**
   ```bash
   curl http://localhost:8000/api/v1/ai/models
   ```

2. **Sprawdź czy modele są włączone:**
   ```yaml
   ai:
     local:
       enabled: true  # Musi być true
     online:
       openai:
         enabled: true
         api_key: "..."  # Musi być ustawiony
   ```

---

## 💬 Problemy z Chatem

### "AI nie rozumie poleceń po polsku"

**Rozwiązania:**

1. **Sprawdź język w konfiguracji:**
   ```yaml
   ai:
     language: "pl"  # Ustaw na "pl"
   ```

2. **Sprawdź command_mapper:**
   ```python
   # src/valetudo/command_mapper.py
   def __init__(self, language: str = "pl"):
       self.language = language
   ```

3. **Użyj jasnych poleceń:**
   - ✅ "Posprzątaj salon"
   - ❌ "Może byś tam przeszedł po salonie"

---

### "Robot nie wykonuje poleceń z chatu"

**Objawy:**
- AI odpowiada, ale robot nic nie robi
- Brak błędów w UI

**Rozwiązania:**

1. **Sprawdź logi backendu:**
   ```bash
   tail -f logs/dreame_x40.log
   ```
   Szukaj: "Failed to execute command"

2. **Sprawdź połączenie z Valetudo:**
   ```bash
   curl http://localhost:8000/api/v1/robot/status
   ```

3. **Przetestuj bezpośrednio:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/robot/start
   ```

4. **Sprawdź confidence threshold:**
   ```python
   # src/api/server.py
   if parsed_command and parsed_command.confidence > 0.7:  # Może obniż?
   ```

---

## 🐛 Problemy ogólne

### "Backend nie startuje"

**Rozwiązania:**

1. **Sprawdź zależności:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Sprawdź Python version:**
   ```bash
   python --version  # Powinno być 3.9+
   ```

3. **Sprawdź czy port jest wolny:**
   ```bash
   # Linux/Mac
   lsof -i :8000

   # Windows
   netstat -ano | findstr :8000
   ```

4. **Sprawdź config file:**
   ```bash
   python -c "from src.config import load_config; print(load_config())"
   ```

---

### "Frontend nie buduje się"

**Rozwiązania:**

1. **Zainstaluj zależności:**
   ```bash
   cd web
   npm install
   ```

2. **Sprawdź Node version:**
   ```bash
   node --version  # Powinno być 16+
   ```

3. **Wyczyść cache:**
   ```bash
   rm -rf node_modules
   rm package-lock.json
   npm install
   ```

4. **Sprawdź błędy TypeScript:**
   ```bash
   npm run build
   ```

---

## 📊 Slow Performance

### "AI odpowiada bardzo wolno"

**Lokalny model:**
1. Zmień na mniejszy model (Mistral 7B → 3B)
2. Użyj niższej quantization (Q8 → Q4)
3. Zamknij inne aplikacje
4. Użyj GPU acceleration w LM Studio

**Online model:**
1. Sprawdź internet: `ping google.com`
2. Zmień model (GPT-4 → GPT-3.5)
3. Zmniejsz `max_tokens`:
   ```yaml
   max_tokens: 1000  # Z 2000
   ```

---

### "Web interface laguje"

1. **Wyczyść historię chatu:**
   - Przycisk "Trash" w interfejsie
   - Lub: `curl -X POST http://localhost:8000/api/v1/ai/clear-history`

2. **Wyłącz auto-polling:**
   ```typescript
   // src/App.tsx
   const interval = setInterval(..., 10000);  // 5000 → 10000ms
   ```

3. **Sprawdź devtools:**
   - F12 → Performance
   - Szukaj bottlenecków

---

## 🔐 Security Issues

### "Exposed API keys in logs"

**Rozwiązanie:**

1. **Użyj .env:**
   ```bash
   # Przenieś klucze z settings.yaml do .env
   OPENAI_API_KEY=sk-...
   ```

2. **Sprawdź .gitignore:**
   ```
   .env
   config/settings.local.yaml
   ```

3. **Nie commituj kluczy:**
   ```bash
   git log --all --full-history -- "*.yaml"
   ```

---

## 📞 Dalsze wsparcie

Jeśli problem nie został rozwiązany:

1. **Sprawdź Issues na GitHub**
2. **Stwórz nowy Issue** z:
   - Opisem problemu
   - Logami (bez API keys!)
   - Wersją systemu, Python, Node
   - Krokami do reprodukcji

3. **Discord/Forum społeczności** (jeśli dostępne)

---

## 🛠️ Przydatne komendy diagnostyczne

```bash
# Sprawdź wszystko
curl http://localhost:8000/api/v1/health
curl http://192.168.1.100  # Valetudo
curl http://192.168.1.50:1234/v1/models  # LM Studio

# Logi
tail -f logs/dreame_x40.log
journalctl -u dreame-x40-ai -f  # Jeśli systemd service

# Network
ping 192.168.1.100
traceroute 192.168.1.100
nmap -p 80,8000,1234 192.168.1.100

# Processes
ps aux | grep python
ps aux | grep node
lsof -i :8000

# Restart wszystkiego
pkill -f "python src/main.py"
pkill -f "npm run dev"
python src/main.py &
cd web && npm run dev &
```
