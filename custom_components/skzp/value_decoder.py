import logging
from homeassistant.const import STATE_UNKNOWN

_LOGGER = logging.getLogger(__name__)

DOMAIN = "skzp"

def decode_value(key: str, raw_value: str) -> str:
    """Główna funkcja dekodująca wartości z SKZP."""

    if key == "DevStatus_Mode":
        return _decode_devstatus_mode(raw_value)
    if key == "DevStatus_Power":
        return _decode_devstatus_power(raw_value)
    if key == "DevStatus_Fan":
        return _decode_devstatus_fan(raw_value)
    if key == "Alarms":
        return _decode_alarms(raw_value)

    return str(raw_value) if raw_value is not None else STATE_UNKNOWN


def _decode_devstatus_mode(raw_value) -> str:
    raw_str = str(raw_value) if raw_value is not None else ""
    if not raw_str or len(raw_str) < 3:
        return STATE_UNKNOWN
    mode = raw_str[0:3].upper()
    mode_map = {
        "PRA": "Praca",
        "CZU": "Czuwanie",
        "MOD": "Modulacja",
        "STO": "Stop",
        "OFF": "Wyłączony",
        "ROZ": "Rozpalanie",
        "WYG": "Wygaszanie",
        "DOP": "Dopalanie",
        "PAU": "Pauza",
        "CZY": "Czyszczenie",
        "KON": "Start palnika",
        "DRE": "Drewno",
        "PRZ": "Przerwa",
    }
    return mode_map.get(mode, f"Nieznany ({mode})")


def _decode_devstatus_power(raw_value) -> int:
    raw_str = str(raw_value) if raw_value is not None else ""
    if not raw_str or len(raw_str) < 6:
        return 0
    try:
        return int(raw_str[3:6])
    except Exception:
        return 0


def _decode_devstatus_fan(raw_value) -> int:
    raw_str = str(raw_value) if raw_value is not None else ""
    if not raw_str or len(raw_str) < 9:
        return 0
    try:
        return int(raw_str[6:9])
    except Exception:
        return 0


def _decode_alarms(raw_value) -> str:
    try:
        raw_str = str(raw_value) if raw_value is not None else ""
        alarm_map = {
            "A": "Przegrzanie kotła",
            "B": "Przegrzanie palnika",
            "C": "Zanik płomienia",
            "D": "Błąd czujnika kotła",
            "E": "Błąd czujnika podajnika",
            "F": "Błąd czujnika spalin",
            "G": "Błąd czujnika mieszacza",
            "H": "Błąd czujnika CWU",
            "I": "Błąd czujnika Obiegu 1",
            "J": "Błąd czujnika Obiegu 2",
            "K": "Błąd czujnika Obiegu 3",
            "M": "Błąd czujnika bufora",
            "P": "Błąd czujnika pokojowego",
            "Q": "Błąd modułu / komunikacji",
            "R": "Blokada tłoka / podajnika",
            "S": "Blokada tłoka (S)",
            "T": "Błąd rozpalania",
            "U": "Rezerwa opału",
            "V": "Błąd czujnika pogodowego",
            "W": "Błąd konf. modułu",
            "Y": "Błąd czujnika pomocniczego Y",
            "Z": "Błąd czujnika pomocniczego Z",
            "1": "Ostrzeżenie 1",
            "2": "Ostrzeżenie 2",
        }

        if not raw_str or raw_str.strip("0") == "":
            return "Brak alarmu"

        active = [desc for code, desc in alarm_map.items() if code in raw_str]

        if not active:
            return f"Nieznany alarm ({raw_str})"

        return ", ".join(active)

    except Exception as e:
        _LOGGER.warning(f"[SKZP] Błąd dekodowania Alarms: {e}")
        return str(raw_value) if raw_value is not None else STATE_UNKNOWN


