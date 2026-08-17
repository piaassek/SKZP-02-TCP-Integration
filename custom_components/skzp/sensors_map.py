# 📌 Mapa znanych kluczy → ładne nazwy, jednostki i dzielniki

SENSOR_MAP = {
    # ✅ Podstawowe dane systemowe
    # "DevId": {"name": "ID urządzenia"},
    # "DevPin": {"name": "PIN urządzenia"},
    "DevType": {"name": "Typ sterownika", "icon": "mdi:chip"},
    # "Token": {"name": "Token sesji"},
    "TimeStamp": {"name": "Czas sterownika", "icon": "mdi:clock-outline"},
    # "FrameType": {"name": "Typ ramki"},
    "DevStatus": {"name": "Surowy status sterownika"},
    "Alarms": {"name": "Alarmy", "icon": "mdi:alert"},
    "UpTime": {"name": "Czas działania", "icon": "mdi:timer"},
    "AN01": {"name": "Sygnał analogowy AN01", "unit": "V", "divider": 100, "icon": "mdi:sine-wave"},

    # 🌡️ Temperatura kotła i spalin
    "BoilerTempAct": {"name": "Temperatura kotła", "unit": "°C", "divider": 100, "icon": "mdi:fire", "state_class": "measurement", "device_class": "temperature"},
    "BoilerTempCmd": {"name": "Zadana temperatura kotła", "unit": "°C", "divider": 100, "icon": "mdi:fire"},
    "ExhaustTempAct": {"name": "Temperatura spalin", "unit": "°C", "divider": 100, "icon": "mdi:smoke", "state_class": "measurement", "device_class": "temperature"},
    # "ExhaustTempMax": {"name": "Maks. temperatura spalin", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-alert"},

    # 💧 CWU
    "DHWTempAct": {"name": "Temperatura CWU", "unit": "°C", "divider": 100, "icon": "mdi:water-boiler", "state_class": "measurement", "device_class": "temperature"},
    "DHWTempCmd": {"name": "Zadana temperatura CWU", "unit": "°C", "divider": 100, "icon": "mdi:water-boiler"},
    "DHWHist": {"name": "Histereza CWU", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-lines"},
    # "DHWMode": {"name": "Tryb CWU", "unit": "", "divider": 1, "icon": "mdi:water"},
    # "DHWPriority": {"name": "Priorytet CWU", "unit": "", "divider": 1, "icon": "mdi:water-check"},
    # "DHWOverH": {"name": "Nadwyżka temperatury CWU", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-plus"},
    # "DHWCMode": {"name": "Tryb cyrkulacji CWU", "unit": "", "divider": 1, "icon": "mdi:water-sync"},
    # "DHWCAlwaysON": {"name": "Cyrkulacja CWU ON", "unit": "", "divider": 1, "icon": "mdi:water-pump"},
    # "DHWCTempON": {"name": "Temp. włączenia cyrkulacji CWU", "unit": "°C", "divider": 100, "icon": "mdi:water-alert"},
    # "DHWCWork": {"name": "Czas pracy cyrkulacji CWU", "unit": "s", "divider": 1, "icon": "mdi:timer"},
    # "DHWCBrake": {"name": "Czas przerwy cyrkulacji CWU", "unit": "s", "divider": 1, "icon": "mdi:timer-off"},

    # --- 🌡️ SKZP-02: CO1 i mieszacz (STARY STEROWNIK) ---
    "CH1ReturnTempAct": {"name": "Temperatura powrotu CO1", "unit": "°C", "divider": 100, "icon": "mdi:radiator", "state_class": "measurement", "device_class": "temperature"},
    "CH1ReturnTempCmd": {"name": "Zadana temperatura powrotu CO1", "unit": "°C", "divider": 100, "icon": "mdi:radiator"},
    # "CH1ReturnProtAct": {"name": "Ochrona powrotu CO1", "unit": "", "divider": 1, "icon": "mdi:shield-check"},
    "CH1MixTempAct": {"name": "Temperatura mieszacza CO1", "unit": "°C", "divider": 100, "icon": "mdi:valve", "state_class": "measurement", "device_class": "temperature"},
    "CH1MixTempCmd": {"name": "Zadana temp. mieszacza CO1", "unit": "°C", "divider": 100, "icon": "mdi:valve"},
    # "CH1MixTempBase": {"name": "Bazowa temp. mieszacza CO1", "unit": "°C", "divider": 100, "icon": "mdi:valve"},
    # "CH1MixTempMin": {"name": "Min. temp. mieszacza CO1", "unit": "°C", "divider": 100, "icon": "mdi:valve"},
    # "CH1MixTempMax": {"name": "Maks. temp. mieszacza CO1", "unit": "°C", "divider": 100, "icon": "mdi:valve"},
    "CH1MixValueAct": {"name": "Pozycja zaworu mieszacza", "unit": "%", "divider": 1, "icon": "mdi:valve"},
    # "CH1MixGain": {"name": "Wzmocnienie mieszacza", "unit": "", "divider": 1, "icon": "mdi:tune"},
    # "CH1MixPeriod": {"name": "Okres pracy siłownika", "unit": "s", "divider": 1, "icon": "mdi:timer"},
    # "CH1MixActive": {"name": "Mieszacz aktywny", "unit": "", "divider": 1, "icon": "mdi:power"},
    "CH1RoomTempAct": {"name": "Temperatura pomieszczenia", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer", "state_class": "measurement", "device_class": "temperature"},
    "CH1RoomTempCmd": {"name": "Zadana temp. pomieszczenia", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer"},
    "CH1RoomTempEco": {"name": "Temp. ECO pomieszczenia", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer-outline"},
    "CH1RoomTempCom": {"name": "Temp. komfortowa pomieszczenia", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer-outline"},
    "CH1RoomHist": {"name": "Histereza pomieszczenia", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-lines"},
    # "CH1Mode": {"name": "Tryb CO1", "unit": "", "divider": 1, "icon": "mdi:heat-wave"},
    # "CH1RoomMode": {"name": "Tryb temperatury pomieszczenia", "unit": "", "divider": 1, "icon": "mdi:calendar-clock"},
    # "CH2Mode": {"name": "Tryb CO2", "unit": "", "divider": 1, "icon": "mdi:heat-wave"},

    # 🌤️ Pogoda
    "WeaTempAct": {"name": "Temperatura zewnętrzna", "unit": "°C", "divider": 100, "icon": "mdi:thermometer", "state_class": "measurement", "device_class": "temperature"},
    # "WeaTempStopCH1": {"name": "Temp. stopu CO1", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-off"},
    # "WeaTempStopCH2": {"name": "Temp. stopu CO2", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-off"},
    # "WeaCorr": {"name": "Korekta pogodowa", "unit": "°C", "divider": 100, "icon": "mdi:weather-windy"},
    # "WeaObjCorr": {"name": "Korekta obiektu", "unit": "", "divider": 1, "icon": "mdi:weather-windy"},

    # 🔥 Paliwo i palnik
    "BuTempAct": {"name": "Temperatura palnika", "unit": "°C", "divider": 100, "icon": "mdi:fire", "state_class": "measurement", "device_class": "temperature"},
    "BuTotalFuel": {"name": "Całkowite zużycie paliwa", "unit": "kg", "divider": 100, "icon": "mdi:factory", "state_class": "total_increasing"},
    "Bu24hFuel": {"name": "Zużycie paliwa 24h", "unit": "kg", "divider": 100, "icon": "mdi:fire-circle", "state_class": "measurement"},
    "BuActualFuel": {"name": "Aktualne spalanie", "unit": "kg/h", "divider": 100, "icon": "mdi:fire-alert", "state_class": "measurement"},
    # "BuModulMin": {"name": "Minimalna modulacja", "unit": "%", "divider": 1, "icon": "mdi:gauge"},
    # "BuModulMax": {"name": "Maksymalna modulacja", "unit": "%", "divider": 1, "icon": "mdi:gauge-full"},
    # "BuTimeAboveMax": {"name": "Czas powyżej max modulacji", "unit": "s", "divider": 1, "icon": "mdi:timer"},
    # "BuAirMin": {"name": "Min. przepływ powietrza", "unit": "%", "divider": 1, "icon": "mdi:fan"},
    # "BuAirMax": {"name": "Max. przepływ powietrza", "unit": "%", "divider": 1, "icon": "mdi:fan"},
    # "BuAditAir": {"name": "Dodatkowe powietrze", "unit": "%", "divider": 1, "icon": "mdi:fan"},
    # "BuFuelCaloric": {"name": "Kaloryczność paliwa", "unit": "MJ/kg", "divider": 1, "icon": "mdi:fire"},
    # "BuFuelCorr": {"name": "Korekta paliwa", "unit": "%", "divider": 1, "icon": "mdi:fire"},
    # "BuMode": {"name": "Tryb palnika", "unit": "", "divider": 1, "icon": "mdi:fire"},
    # "BuSbyPeriod": {"name": "Okres podtrzymania", "unit": "s", "divider": 1, "icon": "mdi:timer"},
    # "BuSbyAirTime": {"name": "Czas nadmuchu w podtrzymaniu", "unit": "s", "divider": 1, "icon": "mdi:timer"},
    # "BuSbyAirPwr": {"name": "Moc powietrza w podtrzymaniu", "unit": "%", "divider": 1, "icon": "mdi:fan"},
    # "BuSbyFeedTime": {"name": "Czas podawania w podtrzymaniu", "unit": "s", "divider": 1, "icon": "mdi:timer"},
    # "BuIntFeedTime": {"name": "Czas podawania w pracy", "unit": "s", "divider": 1, "icon": "mdi:timer"},
    # "BuIntBreakTime": {"name": "Przerwa podawania w pracy", "unit": "s", "divider": 1, "icon": "mdi:timer"},
    # "BuIntAirPwr": {"name": "Moc nadmuchu w pracy", "unit": "%", "divider": 1, "icon": "mdi:fan"},
    # "BuIntHist": {"name": "Histereza palnika", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-lines"},
    # "BuOptNoFireTime": {"name": "Czas bez ognia", "unit": "s", "divider": 1, "icon": "mdi:timer-off"},
    # "BuOptPwr": {"name": "Moc optymalna", "unit": "%", "divider": 1, "icon": "mdi:fire"},
    # "BuOptFdrEff": {"name": "Wydajność podajnika", "unit": "kg/h", "divider": 1, "icon": "mdi:chart-timeline-variant"},
    # "BuOptFdrFTime": {"name": "Czas podawania optymalny", "unit": "s", "divider": 1, "icon": "mdi:timer"},
    # "BuOptClrPeriod": {"name": "Okres czyszczenia", "unit": "s", "divider": 1, "icon": "mdi:timer"},
    # "BuOptClrTime": {"name": "Czas czyszczenia", "unit": "s", "divider": 1, "icon": "mdi:timer"},

    # 🕒 Harmonogramy
    # "DHWDays": {"name": "Dni pracy CWU", "unit": "", "divider": 1, "icon": "mdi:calendar"},
    # "DHWHours": {"name": "Godziny pracy CWU", "unit": "", "divider": 1, "icon": "mdi:calendar-clock"},
    # "DHWCDays": {"name": "Dni pracy cyrkulacji CWU", "unit": "", "divider": 1, "icon": "mdi:calendar"},
    # "DHWCHours": {"name": "Godziny pracy cyrkulacji CWU", "unit": "", "divider": 1, "icon": "mdi:calendar-clock"},
    # "CH1RDays": {"name": "Dni pracy CO1", "unit": "", "divider": 1, "icon": "mdi:calendar"},
    # "CH1RHours": {"name": "Godziny pracy CO1", "unit": "", "divider": 1, "icon": "mdi:calendar-clock"},
    # "CH2Days": {"name": "Dni pracy CO2", "unit": "", "divider": 1, "icon": "mdi:calendar"},
    # "CH2Hours": {"name": "Godziny pracy CO2", "unit": "", "divider": 1, "icon": "mdi:calendar-clock"},

    # 🔧 Dane serwisowe
    # "B026": {"name": "Parametr B026", "unit": "", "divider": 1, "icon": "mdi:tools"},
    # "B059": {"name": "Parametr B059", "unit": "", "divider": 1, "icon": "mdi:tools"},
     "B060": {"name": "Pojemność zasobnika", "unit": "kg", "divider": 1, "icon": "mdi:tools"},
     "B062": {"name": "Pozostałe paliwo", "unit": "kg", "divider": 10, "icon": "mdi:tools"},
    # "K003": {"name": "Parametr K003", "unit": "", "divider": 1, "icon": "mdi:tools"},
    # "K004": {"name": "Parametr K004", "unit": "", "divider": 1, "icon": "mdi:tools"},
    # "K005": {"name": "Parametr K005", "unit": "", "divider": 1, "icon": "mdi:tools"},
    # "K006": {"name": "Parametr K006", "unit": "", "divider": 1, "icon": "mdi:tools"},
    # "K007": {"name": "Parametr K007", "unit": "", "divider": 1, "icon": "mdi:tools"},


    # =========================================================
    # --- 📊 SKZP-05: NOWA GENERACJA STEROWNIKA ---
    # =========================================================

    "C030": {"name": "O1 Zadana temperatura powrotu", "unit": "°C", "divider": 100, "icon": "mdi:radiator"},
    
    # 📊 OBIEG 1 (C0) - np. Grzejniki
    #"C006": {"name": "O1 Temp. mieszacza", "unit": "°C", "divider": 100, "icon": "mdi:valve", "state_class": "measurement", "device_class": "temperature"},
    #"C008": {"name": "O1 Temp. pomieszczenia", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer", "state_class": "measurement", "device_class": "temperature"},
    #"C013": {"name": "O1 Temp. komfortowa", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer"},
    #"C014": {"name": "O1 Temp. ECO", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer-outline"},
    #"C015": {"name": "O1 Histereza", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-lines"},
    #"C027": {"name": "O1 Max temp. mieszacza", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-chevron-up"},
    #"C040": {"name": "O1 Baza krzywej grzewczej", "unit": "°C", "divider": 100, "icon": "mdi:chart-bell-curve"},

    # 📊 OBIEG 2 (C1)
    #"C106": {"name": "O2 Temp. mieszacza", "unit": "°C", "divider": 100, "icon": "mdi:valve", "state_class": "measurement", "device_class": "temperature"},
    #"C108": {"name": "O2 Temp. pomieszczenia", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer", "state_class": "measurement", "device_class": "temperature"},
    #"C113": {"name": "O2 Temp. komfortowa", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer"},
    #"C114": {"name": "O2 Temp. ECO", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer-outline"},
    #"C115": {"name": "O2 Histereza", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-lines"},
    #"C127": {"name": "O2 Max temp. mieszacza", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-chevron-up"},

    # 📊 OBIEG 3 (C2)
    #"C206": {"name": "O3 Temp. mieszacza", "unit": "°C", "divider": 100, "icon": "mdi:valve", "state_class": "measurement", "device_class": "temperature"},
    #"C208": {"name": "O3 Temp. pomieszczenia", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer", "state_class": "measurement", "device_class": "temperature"},
    #"C213": {"name": "O3 Temp. komfortowa", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer"},
    #"C214": {"name": "O3 Temp. ECO", "unit": "°C", "divider": 100, "icon": "mdi:home-thermometer-outline"},
    #"C215": {"name": "O3 Histereza", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-lines"},
    #"C227": {"name": "O3 Max temp. mieszacza", "unit": "°C", "divider": 100, "icon": "mdi:thermometer-chevron-up"},

    # 🛢️ Zewnętrzne źródła ciepła / BUFOR (D2)
    #"D203": {"name": "Temperatura bufora góra", "unit": "°C", "divider": 100, "icon": "mdi:water-boiler", "state_class": "measurement", "device_class": "temperature"},
    #"D204": {"name": "Temperatura bufora dół", "unit": "°C", "divider": 100, "icon": "mdi:water-boiler", "state_class": "measurement", "device_class": "temperature"},
    #"D201": {"name": "Czujnik zewnętrzny D201", "unit": "°C", "divider": 100, "icon": "mdi:thermometer"},
    #"D202": {"name": "Czujnik zewnętrzny D202", "unit": "°C", "divider": 100, "icon": "mdi:thermometer"},
}

# --- Statusy dekodowane przez value_decoder ---
SENSOR_MAP.update({
    "DevStatus_Mode": {"name": "Tryb pracy kotła", "icon": "mdi:state-machine"},
    "DevStatus_Power": {"name": "Moc kotła", "unit": "%", "icon": "mdi:fire", "state_class": "measurement"},
    "DevStatus_Fan": {"name": "Moc dmuchawy", "unit": "%", "icon": "mdi:fan", "state_class": "measurement"},
})
