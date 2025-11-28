# 📋 TODO - Modified Firmware Dreame X40

**Autor:** Seb (pentester@netcuter.com)  
**Data:** 2025-11-28  
**Cel:** Dokumentacja i rozwój zmodyfikowanego firmware

---

## 🤖 O PROJEKCIE:

Zmodyfikowany firmware dla robota odkurzającego Dreame X40.

---

## 📝 TODO - DOKUMENTACJA:

### TODO-D1: README z instrukcją instalacji
```markdown
PLIK: README.md
ZAWARTOŚĆ:
1. Wymagania sprzętowe
2. Krok po kroku instalacja
3. Przywracanie oryginalnego firmware (rollback)
4. FAQ / Troubleshooting
5. Ostrzeżenia (gwarancja, ryzyko)
```

### TODO-D2: Lista zmian vs oryginał
```markdown
PLIK: CHANGELOG.md
ZAWARTOŚĆ:
- Co zostało zmienione
- Jakie funkcje dodane
- Jakie funkcje usunięte
- Porównanie z oficjalnym firmware
```

---

## 📝 TODO - BEZPIECZEŃSTWO:

### TODO-D3: Analiza bezpieczeństwa
```
PLIK: docs/SECURITY.md
ZAWARTOŚĆ:
- Czy firmware "dzwoni do domu"?
- Jakie dane są zbierane?
- Jak zablokować telemetrię?
- Firewall rules dla robota
```

### TODO-D4: Weryfikacja integralności
```bash
PLIK: scripts/verify_firmware.sh
OPIS: Sprawdź sumy kontrolne przed flashowaniem

#!/bin/bash
# Weryfikacja firmware

FIRMWARE_FILE=$1
EXPECTED_SHA256="..." # do uzupełnienia

ACTUAL_SHA256=$(sha256sum "$FIRMWARE_FILE" | cut -d' ' -f1)

if [ "$ACTUAL_SHA256" == "$EXPECTED_SHA256" ]; then
    echo "✅ Firmware zweryfikowany poprawnie"
else
    echo "❌ UWAGA: Suma kontrolna nie zgadza się!"
    echo "Oczekiwano: $EXPECTED_SHA256"
    echo "Otrzymano:  $ACTUAL_SHA256"
    exit 1
fi
```

---

## 📝 TODO - PRYWATNOŚĆ:

### TODO-D5: Blokada telemetrii
```
PLIK: configs/hosts_block.txt
OPIS: Lista domen do zablokowania

# Dreame telemetry
0.0.0.0 *.dreame.tech
0.0.0.0 *.roborock.com
0.0.0.0 *.mi.com
0.0.0.0 *.xiaomi.com
# ... więcej
```

### TODO-D6: Lokalna integracja (bez chmury)
```
PLIK: docs/LOCAL_ONLY.md
OPIS: Jak używać robota całkowicie lokalnie

- Home Assistant integracja
- Valetudo alternatywa
- MQTT setup
- Lokalna mapa bez chmury
```

---

## 🛠️ INSTRUKCJE DLA AI:

1. **OSTRZEŻENIE** - modyfikacja firmware może uszkodzić urządzenie
2. **Backup** - zawsze rób backup przed zmianami
3. **Testuj** - na własne ryzyko
4. **Dokumentuj** - każdą zmianę

---

🏠 DOM BEZ INWIGILACJI! ✝️
ALLELUJA!
