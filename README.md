# SKZP-02 TCP Integration dla Home Assistant

Lokalna integracja TCP dla sterowników kotłów **Timel SKZP-02** w Home Assistant. 

## Funkcje
* 🚀 **Szybkie odświeżanie** — natychmiastowa komunikacja przez gniazdo TCP / konwerter UART-LAN/WiFi.
* 🌡️ **Pełna telemetria** — odczyt temperatur kotła, spalin, powrotu, CWU, CO1/CO2 oraz mieszacza.
* 🎛️ **Sterowanie suwakami (Number)** — zmiana modulacji, zadanej temp. kotła, CWU oraz pokojowej (Com/Eco) z pamięcią stanu po restarcie.
* 🔄 **Zarządzanie pompowanie (Select)** — wygodna lista rozwijana do zmiany trybu pracy CWU (Stop, Auto, Lato, Ciągła praca).
* ⚙️ **Konfiguracja w UI** — prosty instalator przez ekran "Urządzenia i usługi".

## Instalacja przez HACS (Zalecana)
1. Otwórz **HACS** w Home Assistant.
2. Kliknij trzy kropki w prawym górnym rogu i wybierz **Niestandardowe repozytoria** (Custom repositories).
3. Wklej link do tego repozytorium i wybierz kategorię **Integracja** (Integration).
4. Wyszukaj *SKZP-02 TCP* w sklepie HACS, kliknij **Pobierz** i zrestartuj Home Assistanta.
5. Wejdź w **Ustawienia -> Urządzenia i usługi -> Dodaj integrację** i wyszukaj **SKZP**.