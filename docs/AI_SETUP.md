# Konfiguracja AI dla Dreame X40 Assistant

Ten dokument opisuje szczegółową konfigurację AI dla projektu.

## 🎯 Przegląd

Dreame X40 AI Assistant wspiera dwa typy modeli AI:

1. **Lokalny (LM Studio)** - Działa na Twoim komputerze, zero kosztów, pełna prywatność
2. **Online (OpenAI/Claude/Gemini)** - W chmurze, większa moc, wymaga API key

## 🏠 Model Lokalny - LM Studio

### Instalacja LM Studio

1. **Pobierz LM Studio:**
   - Strona: https://lmstudio.ai/
   - Wybierz wersję dla swojego systemu (Windows/Mac/Linux)
   - Zainstaluj

2. **Uruchom LM Studio**

### Pobieranie modelu

1. W LM Studio kliknij **"Search"** (🔍)

2. Zalecane modele dla języka polskiego:

   **Dla słabszych komputerów (8GB RAM):**
   - `TheBloke/Mistral-7B-Instruct-v0.2-GGUF` (4-bit quantization)
   - Wielkość: ~4GB
   - Szybkość: Bardzo dobra
   - Jakość PL: Dobra

   **Dla średnich komputerów (16GB RAM):**
   - `TheBloke/Mistral-7B-Instruct-v0.2-GGUF` (5-bit quantization)
   - `TheBloke/OpenHermes-2.5-Mistral-7B-GGUF`
   - Wielkość: ~5-6GB
   - Szybkość: Dobra
   - Jakość PL: Bardzo dobra

   **Dla mocnych komputerów (32GB+ RAM):**
   - `TheBloke/Llama-2-13B-chat-GGUF`
   - `TheBloke/Nous-Hermes-2-Mixtral-8x7B-DPO-GGUF`
   - Wielkość: 8-16GB
   - Szybkość: Średnia
   - Jakość PL: Wyśmienita

3. Kliknij **Download** przy wybranym modelu

4. Poczekaj na pobranie (może zająć chwilę)

### Uruchomienie serwera lokalnego

1. W LM Studio przejdź do zakładki **"Local Server"** (⚡)

2. Wybierz pobrany model z listy

3. Kliknij **"Start Server"**

4. Server uruchomi się na porcie **1234** (domyślnie)

5. Sprawdź czy działa:
   ```bash
   curl http://localhost:1234/v1/models
   ```

   Powinieneś zobaczyć listę modeli.

### Konfiguracja w projekcie

1. Znajdź IP swojego komputera z LM Studio:

   **Windows:**
   ```cmd
   ipconfig
   ```
   Szukaj "IPv4 Address" (np. 192.168.1.50)

   **Linux/Mac:**
   ```bash
   ifconfig
   # lub
   ip addr
   ```

2. Edytuj `config/settings.yaml`:

   ```yaml
   ai:
     default_model: "local"

     local:
       enabled: true
       host: "192.168.1.50"  # TWÓJ IP
       port: 1234
       model: "local-model"
       timeout: 30
       max_tokens: 2000
       temperature: 0.7
   ```

3. Zapisz i zrestartuj serwer backend

### Testowanie

```bash
# Uruchom backend
python src/main.py

# W logach powinieneś zobaczyć:
# "Local AI client initialized and healthy"
```

## 🌐 Modele Online

### OpenAI (GPT-4, GPT-3.5)

1. **Uzyskaj API Key:**
   - Przejdź do: https://platform.openai.com/api-keys
   - Zaloguj się lub załóż konto
   - Kliknij **"Create new secret key"**
   - Skopiuj klucz (UWAGA: pokaże się tylko raz!)

2. **Konfiguracja:**

   ```yaml
   ai:
     online:
       default_provider: "openai"
       openai:
         enabled: true
         api_key: "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # TWÓJ KLUCZ
         model: "gpt-4"  # lub "gpt-3.5-turbo" (tańszy)
         max_tokens: 2000
         temperature: 0.7
   ```

3. **Koszty (przybliżone):**
   - GPT-3.5 Turbo: ~$0.002 za 1000 tokenów (~500 słów)
   - GPT-4: ~$0.03 za 1000 tokenów
   - GPT-4 Turbo: ~$0.01 za 1000 tokenów

### Anthropic (Claude)

1. **Uzyskaj API Key:**
   - Przejdź do: https://console.anthropic.com/
   - Załóż konto
   - Settings → API Keys → Create Key

2. **Konfiguracja:**

   ```yaml
   ai:
     online:
       default_provider: "anthropic"
       anthropic:
         enabled: true
         api_key: "sk-ant-xxxxxxxxxxxxxxxxxxxxx"  # TWÓJ KLUCZ
         model: "claude-3-5-sonnet-20241022"
         max_tokens: 2000
         temperature: 0.7
   ```

3. **Modele:**
   - `claude-3-5-sonnet-20241022` - Najnowszy, najlepszy
   - `claude-3-haiku-20240307` - Szybszy, tańszy
   - `claude-3-opus-20240229` - Najbardziej zaawansowany

### Google (Gemini)

1. **Uzyskaj API Key:**
   - Przejdź do: https://makersuite.google.com/app/apikey
   - Zaloguj się kontem Google
   - Create API Key

2. **Konfiguracja:**

   ```yaml
   ai:
     online:
       default_provider: "google"
       google:
         enabled: true
         api_key: "AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # TWÓJ KLUCZ
         model: "gemini-pro"
         max_tokens: 2000
         temperature: 0.7
   ```

## 🔄 Przełączanie między modelami

### W web interface

1. Otwórz interfejs: http://localhost:3000
2. W lewym panelu znajdź **"Model AI"**
3. Kliknij na wybrany model
4. Model zostanie przełączony natychmiast

### Przez API

```bash
curl -X POST http://localhost:8000/api/v1/ai/switch-model \
  -H "Content-Type: application/json" \
  -d '{"model": "local"}'
```

Dostępne opcje: `local`, `openai`, `anthropic`, `google`

### Auto-fallback

Jeśli włączone (`auto_fallback: true`), system automatycznie przełączy się na alternatywny model gdy główny nie działa.

Przykład:
- Próba użycia modelu lokalnego
- Lokalny server nie odpowiada
- Automatyczne przełączenie na OpenAI (jeśli skonfigurowane)

## ⚙️ Dostrajanie parametrów

### Temperature (temperatura)

Kontroluje "kreatywność" modelu:

```yaml
temperature: 0.7  # Domyślna
```

- **0.0 - 0.3:** Bardzo przewidywalne, spójne odpowiedzi
- **0.4 - 0.7:** Balans (ZALECANE dla robota)
- **0.8 - 1.0:** Bardzo kreatywne, różnorodne (ryzykowne)

### Max Tokens

Maksymalna długość odpowiedzi:

```yaml
max_tokens: 2000  # ~1500 słów
```

- **500-1000:** Krótkie odpowiedzi
- **1500-2000:** Standardowe (ZALECANE)
- **3000+:** Bardzo długie (droższe dla online)

### Timeout

Czas oczekiwania na odpowiedź (sekundy):

```yaml
timeout: 30  # 30 sekund
```

- Lokalny model: 20-60s (zależy od sprzętu)
- Online: 10-30s

## 🧪 Testowanie konfiguracji

### Test lokalnego modelu

```bash
# Z LM Studio uruchomionym
curl -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local-model",
    "messages": [{"role": "user", "content": "Cześć!"}]
  }'
```

### Test przez Dreame Assistant API

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Jaki jest stan robota?",
    "include_context": true
  }'
```

## 🐛 Rozwiązywanie problemów

### "Local AI client not responding"

1. Sprawdź czy LM Studio server działa
2. Sprawdź IP i port w konfiguracji
3. Sprawdź firewall (port 1234 musi być otwarty)
4. Spróbuj: `curl http://[IP]:1234/v1/models`

### "OpenAI request failed"

1. Sprawdź API key (czy skopiowany poprawnie)
2. Sprawdź limity konta na OpenAI
3. Sprawdź połączenie z internetem

### "Model responses are slow"

**Lokalny:**
- Spróbuj mniejszego modelu lub niższej quantization
- Zamknij inne aplikacje
- Użyj GPU jeśli dostępne (LM Studio → Settings → GPU)

**Online:**
- Sprawdź połączenie internetowe
- Zmień region API (jeśli dostępne)

## 💡 Porady

1. **Dla najlepszej prywatności:** Użyj tylko modelu lokalnego
2. **Dla najlepszej jakości:** Claude 3.5 Sonnet lub GPT-4
3. **Dla balansu:** Model lokalny jako domyślny + OpenAI jako fallback
4. **Dla oszczędności:** GPT-3.5 Turbo lub lokalny Mistral 7B

## 📊 Porównanie modeli

| Model | Prywatność | Koszt | Jakość PL | Szybkość | Wymagania |
|-------|------------|-------|-----------|----------|-----------|
| Mistral 7B (local) | ⭐⭐⭐⭐⭐ | Darmowy | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 8GB RAM |
| Llama 2 13B (local) | ⭐⭐⭐⭐⭐ | Darmowy | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 16GB RAM |
| GPT-3.5 Turbo | ⭐⭐ | $ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Internet |
| GPT-4 | ⭐⭐ | $$$ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Internet |
| Claude 3.5 | ⭐⭐ | $$ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Internet |
| Gemini Pro | ⭐⭐ | $ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Internet |

## 🔐 Bezpieczeństwo API Keys

**NIGDY** nie commituj kluczy API do git!

1. Użyj pliku `.env`:
   ```bash
   cp .env.example .env
   nano .env
   ```

2. Dodaj klucze do `.env`:
   ```
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   GOOGLE_API_KEY=AIza...
   ```

3. Plik `.env` jest w `.gitignore` - bezpieczny!

## 📚 Dodatkowe zasoby

- **LM Studio:** https://lmstudio.ai/docs
- **OpenAI Docs:** https://platform.openai.com/docs
- **Anthropic Docs:** https://docs.anthropic.com/
- **Google AI:** https://ai.google.dev/
