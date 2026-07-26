# SKZP-02 TCP Integration dla Home Assistant

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1+-blue.svg)](https://www.home-assistant.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Lokalna, zaawansowana integracja dla Home Assistant umożliwiająca monitorowanie i pełne sterowanie sterownikiem kotła na paliwo stałe **Timel SKZP-02**. 

Komunikacja odbywa się w czasie rzeczywistym w sieci lokalnej przez strumień TCP, z wykorzystaniem konwertera UART-LAN / WiFi (RS-232 na TCP). Integracja posiada wbudowany bufor sieciowy, dzięki czemu jest całkowicie odporna na uszkodzone lub niepełne ramki danych.

---

## ✨ Główna funkcjonalność

* 🚀 **Szybka i lokalna komunikacja TCP** — natychmiastowy odczyt parametrów pracy pieca bez chmury i opóźnień.
* 📊 **Bogata telemetria (Sensory)** — ponad 30 czujników odczytujących m.in. temperatury kotła, spalin, powrotu, CWU, CO1, mieszacza, a także zużycie paliwa (chwilowe, 24h, całkowite) oraz stan zasobnika.
* 🔘 **Statusy urządzeń (Binary Sensors)** — dwustanowe czujniki informujące o pracy podajnika, dmuchawy, pompy CO, pompy CWU oraz o stanie alarmów.
* 🎛️ **Zdalne sterowanie (Number)** — suwaki na Dashboardzie z pamięcią stanu po restarcie dla zadanego CO, zadanego CWU, temperatur pokojowych (Komfort / Eco) oraz minimalnej modulacji palnika.
* 🔄 **Wybór trybu pracy (Select)** — rozwijana lista umożliwiająca zmianę trybu podgrzewacza wody (CWU): *Stop*, *Auto*, *Lato*, *Cyrkulacja*.
* 🛡️ **Zgodność z najnowszymi standardami HA** — polskie nazwy na kartach i wykresach przy jednoczesnym automatycznym generowaniu czystych identyfikatorów systemowych bez polskich znaków (np. `sensor.skzp_temperatura_kotla`). Pełna zachowalność historii wykresów!
* ⚙️ **Prosta konfiguracja w UI** — instalacja i zmiana parametrów (IP/Port) bezpośrednio w interfejsie graficznym Home Assistanta.
<img width="520" height="1024" alt="671957794_26340330608980783_6767839624693781370_n" src="https://github.com/user-attachments/assets/9dad167d-47a0-4bd5-be86-8865803f8716" />
---

## 📥 Instalacja przez HACS (Zalecana)

Integracja jest przystosowana do instalacji przez **HACS (Home Assistant Community Store)**, co zapewnia automatyczne powiadomienia o nowych wersjach i aktualizacje jednym kliknięciem.

### Krok 1: Dodanie repozytorium do HACS
1. Otwórz panel **HACS** w Home Assistant.
2. Kliknij ikonkę **trzech kropek (`...`)** w prawym górnym rogu i wybierz **Niestandardowe repozytoria** (Custom repositories).
3. Wklej adres URL tego repozytorium (np. `https://github.com/TWOJA_NAZWA/SKZP-02-TCP-Integration`).
4. Jako kategorię wybierz obowiązkowo: **Integracja (Integration)** i kliknij **Dodaj**.

### Krok 2: Pobranie i restart
1. Wyszukaj **SKZP-02 TCP** w sklepie HACS, kliknij w nią i wybierz niebieski przycisk **Pobierz** (Download).
2. Wykonaj **pełny restart Home Assistanta** (*Ustawienia* ➔ *System* ➔ ikonka zasilania ➔ *Uruchom ponownie Home Assistant*). Jest to niezbędne, aby system wczytał nowe pliki z katalogu `custom_components`.

### Krok 3: Konfiguracja połączenia w interfejsie
1. Po restarcie wciśnij `Ctrl + F5` (lub `Cmd + Shift + R`), aby odświeżyć pamięć podręczną przeglądarki.
2. Przejdź do: **Ustawienia** ➔ **Urządzenia i usługi**.
3. Kliknij niebieski przycisk **+ Dodaj integrację** w prawym dolnym rogu.
4. Wyszukaj i wybierz **SKZP**.
5. W oknie konfiguratora podaj:
   * **Host:** Adres IP Twojego konwertera w sieci lokalnej (np. `192.168.1.157`).
   * **Port:** Port nasłuchu konwertera TCP (np. `1515` lub `80`).
6. Kliknij **Zatwierdź**. Wszystkie dostępne czujniki i suwaki zostaną automatycznie dodane do Twojego systemu!

---

## 🛠️ Personalizacja czujników (`sensors_map.py`)

Integracja działa od razu po instalacji i automatycznie tworzy wszystkie najważniejsze encje. Możesz jednak bardzo łatwo włączyć dodatkowe parametry serwisowe lub wyłączyć czujniki, z których nie korzystasz.

W folderze integracji (`/config/custom_components/skzp/`) znajduje się plik **`sensors_map.py`**. Zawiera on pełną mapę parametrów wysyłanych przez sterownik:

```python
    # Przykład aktywnego sensora (widoczny w HA):
    "ExhaustTempAct": {"name": "Temperatura spalin", "unit": "°C", "divider": 100, "icon": "mdi:smoke", "state_class": "measurement", "device_class": "temperature"},

    # Przykład nieaktywnego sensora (ukryty w HA):
    # "ExhaustTempMax": {"name": "Maks. temperatura spalin", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-alert"},



