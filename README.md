# SKZP TCP Integration dla Home Assistant

Lokalna integracja TCP dla sterowników kotłów **Timel SKZP-02 / SKZP-05** w Home Assistant. 

## Funkcje
* 🚀 **Szybkie odświeżanie** — natychmiastowa komunikacja przez gniazdo TCP / konwerter UART-LAN/WiFi.
* 🌡️ **Pełna telemetria** — odczyt temperatur kotła, spalin, powrotu, CWU, CO1/CO2/CO3 oraz mieszaczy.
* 🎛️ **Sterowanie suwakami (Number)** — zmiana modulacji, zadanej temp. kotła, CWU oraz pokojowej (Com/Eco) z pamięcią stanu po restarcie.
* 🔄 **Zarządzanie pompą CWU (Select)** — lista rozwijana do zmiany trybu pracy pompy CWU (Stop, Auto, Timer, Ciągła praca).
* ⚙️ **Konfiguracja w UI** — prosty instalator przez ekran "Urządzenia i usługi" z obsługą numeru PIN.

## Instalacja przez HACS (Zalecana)
1. Otwórz **HACS** w Home Assistant.
2. Kliknij trzy kropki w prawym górnym rogu i wybierz **Niestandardowe repozytoria** (Custom repositories).
3. Wklej link: `https://github.com/piaassek/SKZP-02-TCP-Integration` i wybierz kategorię **Integracja** (Integration).
4. Wyszukaj *SKZP TCP Integration* w sklepie HACS, kliknij **Pobierz** i zrestartuj Home Assistanta.
5. Wejdź w **Ustawienia -> Urządzenia i usługi -> Dodaj integrację** i wyszukaj **SKZP**.

