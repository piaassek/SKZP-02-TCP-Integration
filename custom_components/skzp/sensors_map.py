# 📌 Mapa znanych kluczy → ładne nazwy, jednostki i dzielniki dla SKZP-02 i SKZP-05

SENSOR_MAP = {
    # ✅ Podstawowe dane systemowe
    "DevType": {"name": "Typ sterownika", "icon": "mdi:chip"},
    "TimeStamp": {"name": "Czas sterownika", "icon": "mdi:clock-outline"},
    "DevStatus": {"name": "Surowy status sterownika"},
    "Alarms": {"name": "Alarmy", "icon": "mdi:alert"},
    "UpTime": {"name": "Czas działania", "icon": "mdi:timer"},
    "AN01": {"name": "Sygnał analogowy AN01", "unit": "V", "divider": 100, "icon": "mdi:sine-wave"},

    # 🌡️ Temperatura kotła i spalin (Wspólne)
    "BoilerTempAct": {"name": "Temperatura kotła", "unit": "°C", "divider": 100, "icon": "mdi:fire", "state_class": "measurement", "device_class": "temperature"},
    "BoilerTempCmd": {"name": "Zadana temperatura kotła", "unit": "°C", "divider": 100, "icon": "mdi:fire"},
    "ExhaustTempAct": {"name": "Temperatura spalin", "unit": "°C", "divider": 100, "icon": "mdi:smoke", "state_class": "measurement", "device_class": "temperature"},
    "ExhaustTempMax": {"name": "Maks. temperatura spalin", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-alert"},

    # 💧 CWU (Wspólne)
    "DHWTempAct": {"name": "Temperatura CWU", "unit": "°C", "divider": 100, "icon": "mdi:water-boiler", "state_class": "measurement", "device_class": "temperature"},
    "DHWTempCmd": {"name": "Zadana temperatura CWU", "unit": "°C", "divider": 100, "icon": "mdi:water-boiler"},
    "DHWHist": {"name": "Histereza CWU", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-lines"},
    "DHWOverH": {"name": "Nadwyżka temperatury CWU", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-plus"},
    "DHWCTempON": {"name": "Temp. włączenia cyrkulacji CWU", "unit": "°C", "divider": 100, "icon": "mdi:water-alert"},
    "DHWCWork": {"name": "Czas pracy cyrkulacji CWU", "unit": "s", "divider": 1, "icon": "mdi:timer"},
    "DHWCBrake": {"name": "Czas przerwy cyrkulacji CWU", "unit": "s", "divider": 1, "icon": "mdi:timer-off"},

    # 🌤️ Pogoda (Wspólne)
    "WeaTempAct": {"name": "Temperatura zewnętrzna", "unit": "°C", "divider": 100, "icon": "mdi:thermometer", "state_class": "measurement", "device_class": "temperature"},

    # 🔥 Paliwo i palnik (Wspólne)
    "BuTempAct": {"name": "Temperatura palnika", "unit": "°C", "divider": 100, "icon": "mdi:fire", "state_class": "measurement", "device_class": "temperature"},
    "BuTotalFuel": {"name": "Całkowite zużycie paliwa", "unit": "kg", "divider": 100, "icon": "mdi:factory", "state_class": "total_increasing"},
    "Bu24hFuel": {"name": "Zużycie paliwa 24h", "unit": "kg", "divider": 100, "icon": "mdi:fire-circle", "state_class": "measurement"},
    "BuActualFuel": {"name": "Aktualne spalanie", "unit": "kg/h", "divider": 100, "icon": "mdi:fire-alert", "state_class": "measurement"},
    "BuFuelCaloric": {"name": "Kaloryczność paliwa", "unit": "MJ/kg", "divider": 1, "icon": "mdi:fire"},
    "BuFuelCorr": {"name": "Korekta paliwa", "unit": "%", "divider": 1, "icon": "mdi:fire"},
    "B060": {"name": "Pojemność zasobnika", "unit": "kg", "divider": 1, "icon": "mdi:tools"},
    "B062": {"name": "Pozostałe paliwo", "unit": "kg", "divider": 10, "icon": "mdi:tools"},
    "B059": {"name": "Rezerwa paliwa", "unit": "kg", "divider": 1, "icon": "mdi:tools"},

    # =========================================================
    # --- 🌡️ SKZP-02: Dedykowane sensory (Obieg 1 / CH1) ---
    # =========================================================
    "CH1ReturnTempAct": {"name": "Temperatura powrotu", "unit": "°C", "divider": 100, "icon": "mdi:radiator", "state_class": "measurement", "device_class": "temperature"},
    "CH1ReturnTempCmd": {"name": "Zadana temperatura powrotu (SKZP-02)", "unit": "°C", "divider": 100, "icon": "mdi:radiator"},
    "CH1MixTempAct": {"name": "Temperatura mieszacza (SKZP-02)", "unit": "°C", "divider": 100, "icon": "mdi:valve", "state_class": "measurement", "device_class": "temperature"},
    "CH1MixTempCmd": {"name": "Zadana temp. mieszacza (SKZP-02)", "unit": "°C", "divider": 100, "icon": "mdi:valve"},
    "CH1MixValueAct": {"name": "Pozycja zaworu mieszacza (SKZP-02)", "unit": "%", "divider": 1, "icon": "mdi:valve"},
    "CH1RoomTempAct": {"name": "Temperatura pomieszczenia (SKZP-02)", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer", "state_class": "measurement", "device_class": "temperature"},
    "CH1RoomTempCmd": {"name": "Zadana temp. pomieszczenia (SKZP-02)", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer"},
    "CH1RoomTempEco": {"name": "Temp. ECO pomieszczenia (SKZP-02)", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer-outline"},
    "CH1RoomTempCom": {"name": "Temp. komfortowa pomieszczenia (SKZP-02)", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer-outline"},
    "CH1RoomHist": {"name": "Histereza pomieszczenia (SKZP-02)", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-lines"},

    # =========================================================
    # --- 📊 SKZP-05: Dedykowane sensory (Obiegi C0, C1, C2 + Bufor D2) ---
    # =========================================================
    # 📊 OBIEG 1 (C0)
    "C006": {"name": "O1 Temp. mieszacza", "unit": "°C", "divider": 100, "icon": "mdi:valve", "state_class": "measurement", "device_class": "temperature"},
    "C008": {"name": "O1 Temp. pomieszczenia", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer", "state_class": "measurement", "device_class": "temperature"},
    "C013": {"name": "O1 Temp. komfortowa", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer"},
    "C014": {"name": "O1 Temp. ECO", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer-outline"},
    "C015": {"name": "O1 Histereza", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-lines"},
    "C027": {"name": "O1 Max temp. mieszacza", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-chevron-up"},
    "C028": {"name": "O1 Min temp. mieszacza", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-chevron-down"},
    "C030": {"name": "O1 Zadana temperatura powrotu", "unit": "°C", "divider": 100, "icon": "mdi:radiator"},
    "C040": {"name": "O1 Baza krzywej grzewczej", "unit": "°C", "divider": 100, "icon": "mdi:chart-bell-curve"},

    # 📊 OBIEG 2 (C1)
    "C106": {"name": "O2 Temp. mieszacza", "unit": "°C", "divider": 100, "icon": "mdi:valve", "state_class": "measurement", "device_class": "temperature"},
    "C108": {"name": "O2 Temp. pomieszczenia", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer", "state_class": "measurement", "device_class": "temperature"},
    "C113": {"name": "O2 Temp. komfortowa", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer"},
    "C114": {"name": "O2 Temp. ECO", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer-outline"},
    "C115": {"name": "O2 Histereza", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-lines"},
    "C127": {"name": "O2 Max temp. mieszacza", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-chevron-up"},
    "C128": {"name": "O2 Min temp. mieszacza", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-chevron-down"},
    "C140": {"name": "O2 Baza krzywej grzewczej", "unit": "°C", "divider": 100, "icon": "mdi:chart-bell-curve"},

    # 📊 OBIEG 3 (C2)
    "C206": {"name": "O3 Temp. mieszacza", "unit": "°C", "divider": 100, "icon": "mdi:valve", "state_class": "measurement", "device_class": "temperature"},
    "C208": {"name": "O3 Temp. pomieszczenia", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer", "state_class": "measurement", "device_class": "temperature"},
    "C213": {"name": "O3 Temp. komfortowa", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer"},
    "C214": {"name": "O3 Temp. ECO", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer-outline"},
    "C215": {"name": "O3 Histereza", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-lines"},
    "C227": {"name": "O3 Max temp. mieszacza", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-chevron-up"},
    "C228": {"name": "O3 Min temp. mieszacza", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-chevron-down"},
    "C240": {"name": "O3 Baza krzywej grzewczej", "unit": "°C", "divider": 100, "icon": "mdi:chart-bell-curve"},

    # 🛢️ BUFOR / Zewnętrzne źródła ciepła (D2)
    "D203": {"name": "Temperatura bufora góra", "unit": "°C", "divider": 100, "icon": "mdi:water-boiler", "state_class": "measurement", "device_class": "temperature"},
    "D204": {"name": "Temperatura bufora dół", "unit": "°C", "divider": 100, "icon": "mdi:water-boiler", "state_class": "measurement", "device_class": "temperature"},
    "D201": {"name": "Czujnik zewnętrzny D201", "unit": "°C", "divider": 100, "icon": "mdi:thermometer", "state_class": "measurement", "device_class": "temperature"},
    "D202": {"name": "Czujnik zewnętrzny D202", "unit": "°C", "divider": 100, "icon": "mdi:thermometer", "state_class": "measurement", "device_class": "temperature"},
}

# --- Statusy dekodowane przez value_decoder ---
SENSOR_MAP.update({
    "DevStatus_Mode": {"name": "Tryb pracy kotła", "icon": "mdi:state-machine"},
    "DevStatus_Power": {"name": "Moc kotła", "unit": "%", "icon": "mdi:fire", "state_class": "measurement"},
    "DevStatus_Fan": {"name": "Moc dmuchawy", "unit": "%", "icon": "mdi:fan", "state_class": "measurement"},
})

