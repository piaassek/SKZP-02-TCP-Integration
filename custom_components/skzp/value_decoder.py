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


def _decode_devstatus_mode(raw_value: str) -> str:
    if not raw_value or len(raw_value) < 3:
        return STATE_UNKNOWN
    mode = raw_value[0:3]
    mode_map = {
        "PRA": "Praca",
        "CZU": "Czuwanie",
        "MOD": "Modulacja",
        "STO": "Stop",
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


def _decode_devstatus_power(raw_value: str) -> int:
    if not raw_value or len(raw_value) < 6:
        return 0
    try:
        return int(raw_value[3:6])
    except Exception:
        return 0


def _decode_devstatus_fan(raw_value: str) -> int:
    if not raw_value or len(raw_value) < 9:
        return 0
    try:
        return int(raw_value[6:9])
    except Exception:
        return 0


def _decode_alarms(raw_value: str) -> str:
    try:
        alarm_map = {
            "A": "Przegrzanie kotła",
            "B": "Przegrzanie palnika",
            "C": "Zanik płomienia",
            "D": "Błąd czujnika kotła",
            "E": "Błąd czujnika podajnika",
            "F": "Błąd czujnika spalin",
            "G": "Błąd czujnika mieszacza",
            "H": "Błąd czujnika CWU",
            "P": "Błąd czujnika pokojowego",
            "R": "Blokada tłoka",
            "S": "Blokada tłoka (S)",
            "T": "Błąd rozpalania",
            "U": "Rezerwa opału",
            "W": "Błąd konf. modułu",
        }

        if not raw_value or raw_value.strip("0") == "":
            return "Brak alarmu"

        active = [desc for code, desc in alarm_map.items() if code in raw_value]

        if not active:
            return f"Nieznany alarm ({raw_value})"

        return ", ".join(active)

    except Exception as e:
        _LOGGER.warning(f"[SKZP] Błąd dekodowania Alarms: {e}")
        return str(raw_value) if raw_value else STATE_UNKNOWN
