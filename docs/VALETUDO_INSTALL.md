# Instalacja Valetudo na Dreame X40

Ten dokument opisuje proces instalacji Valetudo na Dreame X40 Complete.

## ⚠️ Ostrzeżenie

**UWAGA:** Proces rootowania może:
- Unieważnić gwarancję producenta
- Potencjalnie uszkodzić robota (brick)
- Wymagać pewnych umiejętności technicznych

Postępuj ostrożnie i na własne ryzyko!

## 📋 Wymagania

### Hardware
- Dreame X40 Complete (fabrycznie nowy lub po resecie)
- Komputer z systemem Windows/Linux/Mac
- Kabel USB-C do podłączenia robota (opcjonalnie, zależy od metody)

### Software
- Dostęp do internetu
- Przeglądarka internetowa

## 🔧 Metoda 1: Dustbuilder (Zalecana)

Dustbuilder to narzędzie webowe do tworzenia zrootowanego firmware dla robotów Dreame.

### Krok 1: Sprawdź wersję firmware

1. Otwórz aplikację Dreame/Xiaomi Home
2. Przejdź do ustawień robota
3. Sprawdź wersję firmware
4. Zanotuj pełną wersję (np. 4.2.8_1234)

### Krok 2: Uzyskaj token i DID

Metoda zależy od aplikacji:

**Dla Xiaomi Home:**
1. Zainstaluj aplikację do ekstrakcji tokena (np. "Xiaomi Cloud Tokens Extractor")
2. Uruchom i zaloguj się swoimi danymi Xiaomi
3. Znajdź swojego robota i zanotuj `token` oraz `did`

**Dla Dreame App:**
1. Token można uzyskać przez analizę logów aplikacji
2. Szczegóły: https://valetudo.cloud/pages/general/rooting-instructions.html

### Krok 3: Dustbuilder

1. Otwórz: https://builder.dontvacuum.me/
2. Wybierz producenta: **Dreame**
3. Wybierz model: **Dreame X40 / L40 Ultra**
4. Wybierz wersję firmware (ta sama co w kroku 1)
5. Zaznacz opcje:
   - ✅ **Valetudo** (najnowsza wersja)
   - ✅ **Disable firmware updates** (zalecane)
   - ✅ **Prepackage Valetudo** (łatwiejsza instalacja)
6. Kliknij **Create Job**
7. Poczekaj na zbudowanie firmware (może zająć kilka minut)
8. Pobierz wygenerowany firmware (.pkg)

### Krok 4: Instalacja firmware

1. Umieść plik .pkg na serwerze HTTP lub użyj Dustbuilder proxy
2. W aplikacji Dreame/Xiaomi Home:
   - Przejdź do ustawień robota
   - Znajdź opcję aktualizacji firmware
   - Podaj URL do pliku .pkg

**LUB**

3. Użyj narzędzia do ręcznej instalacji (wymaga dostępu przez SSH)

### Krok 5: Pierwszy rozruch

1. Po instalacji robot się zrestartuje
2. Poczekaj kilka minut
3. Valetudo powinno być dostępne pod adresem IP robota
4. Sprawdź: `http://[IP_ROBOTA]`

## 🔧 Metoda 2: UART/Fastboot (Zaawansowana)

Ta metoda wymaga:
- Rozmontowania robota
- Podłączenia do pinów UART
- Specjalistycznego sprzętu

**Dokumentacja:**
- https://valetudo.cloud/pages/installation/dreame.html
- https://dontvacuum.me/robotinfo/

## ✅ Weryfikacja instalacji

Po instalacji Valetudo:

1. Sprawdź dostęp do web interface:
   ```
   http://[IP_ROBOTA]
   ```

2. Powinieneś zobaczyć interfejs Valetudo z mapą i kontrolkami

3. Sprawdź czy robot działa:
   - Mapa się generuje
   - Można wysłać polecenie start/stop
   - MQTT działa (jeśli skonfigurowane)

## 📝 Konfiguracja Valetudo

### Podstawowa konfiguracja

1. Otwórz Valetudo: `http://[IP_ROBOTA]`
2. Przejdź do **Settings**
3. Skonfiguruj:
   - **Connectivity → Wi-Fi:** Sprawdź połączenie
   - **Connectivity → MQTT:** Włącz jeśli chcesz integracji z Home Assistant
   - **Map → Settings:** Dostosuj ustawienia mapy

### MQTT (Opcjonalnie)

Jeśli chcesz używać MQTT:

1. Zainstaluj MQTT broker (np. Mosquitto)
2. W Valetudo → Settings → MQTT:
   - Server: `mqtt://[IP_BROKERA]:1883`
   - Username/Password (jeśli wymagane)
   - Base topic: `valetudo`

## 🔄 Aktualizacja Valetudo

Valetudo można aktualizować bez ponownego rootowania:

1. Otwórz Valetudo
2. Settings → Updater
3. Sprawdź dostępne aktualizacje
4. Kliknij **Update**

## 🆘 Rozwiązywanie problemów

### Robot nie odpowiada

1. Sprawdź czy robot jest podłączony do Wi-Fi
2. Sprawdź IP robota w routerze
3. Spróbuj pingować: `ping [IP_ROBOTA]`

### Valetudo nie działa

1. Sprawdź logi:
   ```bash
   ssh root@[IP_ROBOTA]
   cat /var/log/upstart/valetudo.log
   ```

2. Zrestartuj Valetudo:
   ```bash
   ssh root@[IP_ROBOTA]
   initctl restart valetudo
   ```

### Brak dostępu SSH

Domyślne dane logowania (po rootowaniu):
- Username: `root`
- Password: Wygenerowane przez Dustbuilder (sprawdź w logach budowania)

## 📚 Dodatkowe zasoby

- **Dokumentacja Valetudo:** https://valetudo.cloud/
- **Discord Valetudo:** https://discord.gg/valetudo
- **Reddit r/Valetudo:** https://reddit.com/r/Valetudo
- **Don't Vacuum Wiki:** https://dontvacuum.me/

## ⚡ Następne kroki

Po zainstalowaniu Valetudo możesz:

1. Zainstalować **Dreame X40 AI Assistant** (ten projekt)
2. Zintegrować z **Home Assistant**
3. Tworzyć automatyzacje
4. Używać lokalnej kontroli bez chmury

Przejdź do głównego README projektu: [README.md](../README.md)
