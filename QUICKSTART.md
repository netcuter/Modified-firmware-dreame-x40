# 🚀 Quick Start Guide

Szybki start dla Dreame X40 AI Assistant w 5 minut!

## ⚡ Minimalna konfiguracja

### 1. Wymagania wstępne

**WAŻNE:** Potrzebujesz Dreame X40 z zainstalowanym Valetudo!
- Jeśli nie masz: [VALETUDO_INSTALL.md](docs/VALETUDO_INSTALL.md)

**Software:**
- Python 3.9+ ✅
- Node.js 18+ ✅
- LM Studio (dla modelu lokalnego) 🔧

### 2. Instalacja (2 minuty)

```bash
# Clone repo (jeśli jeszcze nie masz)
git clone <your-repo-url>
cd Modified-firmware-dreame-x40

# Backend
pip install -r requirements.txt

# Frontend
cd web
npm install
cd ..
```

### 3. Podstawowa konfiguracja (1 minuta)

Edytuj `config/settings.yaml`:

```yaml
valetudo:
  host: "192.168.1.XXX"  # ← IP Twojego robota!

ai:
  default_model: "local"  # lub "online" jeśli masz API key

  local:
    host: "192.168.1.YYY"  # ← IP komputera z LM Studio
    port: 1234
```

### 4. Uruchom (1 minuta)

**Terminal 1 - Backend:**
```bash
python src/main.py
```

**Terminal 2 - Frontend:**
```bash
cd web
npm run dev
```

### 5. Otwórz przeglądarką

```
http://localhost:3000
```

## 🎉 Gotowe!

Teraz możesz:
- ✅ Rozmawiać z robotem po polsku
- ✅ Wydawać polecenia głosowe
- ✅ Przełączać między modelami AI
- ✅ Kontrolować robota przez UI

## 📝 Przykłady

**W chatcie napisz:**
- "Posprzątaj salon"
- "Jaki jest stan baterii?"
- "Wróć do stacji"

## 🔧 Opcjonalna konfiguracja

### Dodaj OpenAI (zalecane jako backup)

1. Uzyskaj klucz: https://platform.openai.com/api-keys

2. Dodaj do `config/settings.yaml`:
```yaml
ai:
  online:
    openai:
      enabled: true
      api_key: "sk-..." # Twój klucz
```

3. Włącz auto-fallback:
```yaml
ai:
  auto_fallback: true  # Automatyczne przełączanie gdy local nie działa
```

## 🆘 Problemy?

**Backend nie startuje?**
```bash
pip install -r requirements.txt  # Zainstaluj ponownie
```

**Frontend nie działa?**
```bash
cd web
rm -rf node_modules
npm install
```

**Nie łączy się z robotem?**
- Sprawdź IP robota w `config/settings.yaml`
- Ping: `ping 192.168.1.XXX`
- Otwórz Valetudo: `http://192.168.1.XXX`

**AI nie odpowiada?**
- Sprawdź czy LM Studio server działa
- Sprawdź IP w konfiguracji
- Test: `curl http://192.168.1.YYY:1234/v1/models`

## 📚 Więcej informacji

- **Pełna dokumentacja:** [README.md](README.md)
- **Konfiguracja AI:** [docs/AI_SETUP.md](docs/AI_SETUP.md)
- **Lista poleceń:** [docs/COMMANDS.md](docs/COMMANDS.md)
- **Rozwiązywanie problemów:** [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

## 💡 Pro Tips

1. **Ustaw statyczny IP dla robota** w routerze
2. **Użyj lokalnego modelu jako domyślnego** (prywatność + szybkość)
3. **Dodaj OpenAI jako backup** (auto-fallback gdy local nie działa)
4. **Testuj polecenia w Valetudo** najpierw, potem przez AI

---

**Miłego sprzątania! 🤖✨**
