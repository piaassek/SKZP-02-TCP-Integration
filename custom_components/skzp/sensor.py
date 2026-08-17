import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.core import callback

from .const import DOMAIN
from .sensors_map import SENSOR_MAP
from .value_decoder import decode_value

_LOGGER = logging.getLogger(__name__)

DIAGNOSTIC_KEYS = {"DevType", "TimeStamp", "DevStatus", "Alarms", "UpTime"}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Inicjalizacja sensorów SKZP zależnie od wykrytego modelu."""
    client = hass.data[DOMAIN]["client"]
    entities = []

    is_05 = client.is_skzp05
    is_02 = not is_05

    for key, meta in SENSOR_MAP.items():
        if "name" not in meta:
            continue

        # Dla SKZP-02 pomijamy sensory specyficzne dla SKZP-05 (C0xx, C1xx, C2xx, D2xx)
        if is_02 and (key.startswith(("C0", "C1", "C2", "D2"))):
            continue

        # Dla SKZP-05 pomijamy sensory specyficzne dla SKZP-02 (CH1Mix, CH1Room)
        if is_05 and (key.startswith(("CH1Mix", "CH1Room"))):
            continue

        # Jeśli mamy dane ze sterownika, dodaj tylko te sensory, które faktycznie występują w ramce (lub wirtualne DevStatus_)
        if client.data and (key not in client.data and not key.startswith("DevStatus_")):
            continue

        meta.setdefault("divider", None)
        meta.setdefault("unit", None)
        meta.setdefault("icon", None)
        meta.setdefault("device_class", None)
        meta.setdefault("state_class", None)

        entities.append(SkzpSensor(client, key, meta))

    async_add_entities(entities)
    _LOGGER.info(f"[SKZP] Dodano {len(entities)} sensorów dla modelu {'SKZP-05' if is_05 else 'SKZP-02'}.")



class SkzpSensor(SensorEntity):
    """Encja sensora SKZP."""

    _attr_should_poll = False

    def __init__(self, client, key, meta):
        self._client = client
        self._key = key
        self._attr_name = meta.get("name")
        self.entity_id = f"sensor.skzp_{key.lower()}"
        self._attr_unique_id = f"skzp_{key.lower()}"
        self._attr_native_unit_of_measurement = meta.get("unit") 
        self._divider = meta.get("divider")
        self._attr_icon = meta.get("icon")
        self._remove_listener = None

        if meta.get("state_class"):
            self._attr_state_class = meta["state_class"]
        if meta.get("device_class"):
            self._attr_device_class = meta["device_class"]

        if key in DIAGNOSTIC_KEYS:
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_added_to_hass(self):
        """Podpięcie nasłuchiwania danych po dodaniu encji do HA."""
        self._remove_listener = self._client.hass.bus.async_listen(
            f"{DOMAIN}_data_update", self._handle_data_update
        )
        self._handle_data_update(None)

    @callback
    def _handle_data_update(self, event):
        raw_value = self._client.data.get(self._key)
        
        # Obsługa statusów wirtualnych (Mode, Power, Fan)
        if self._key.startswith("DevStatus_") and raw_value is None:
            raw_value = self._client.data.get("DevStatus", "")
        
        # Jeśli parametr nie przyszedł w ramce (np. specyficzny dla innego modelu)
        if raw_value is None:
            self._attr_available = False
            self._attr_native_value = None
            self.async_write_ha_state()
            return

        # Wartość 30000 lub 9999 w sterownikach Timel oznacza odłączony / nieaktywny czujnik
        if str(raw_value).strip() in ("30000", "9999"):
            self._attr_available = False
            self._attr_native_value = None
            self.async_write_ha_state()
            return

        self._attr_available = True

        # Dekodowanie wartości tekstowych (np. Alarms, DevStatus_Mode)
        decoded = decode_value(self._key, raw_value)

        # Jeśli dekoder zwrócił przetłumaczoną wartość inną niż wejściowa
        if decoded != str(raw_value):
            self._attr_native_value = decoded
            self.async_write_ha_state()
            return

        # Obsługa liczb i dzielnika
        if self._divider:
            try:
                value = float(raw_value) / self._divider
                self._attr_native_value = round(value, 2)
            except (ValueError, TypeError):
                self._attr_native_value = None
        else:
            self._attr_native_value = str(raw_value)

        self.async_write_ha_state()

    async def async_will_remove_from_hass(self):
        if self._remove_listener:
            self._remove_listener()

    @property
    def device_info(self):
        dev_type = self._client.data.get("DevType", "SKZP")
        model = "SKZP-05" if "05" in str(dev_type) else ("SKZP-02" if "02" in str(dev_type) else "SKZP")
        return {
            "identifiers": {(DOMAIN, "skzp_device")},
            "name": f"Sterownik {model}",
            "manufacturer": "Timel",
            "model": str(dev_type),
        }
