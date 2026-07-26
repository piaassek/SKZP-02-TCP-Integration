import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.core import callback

from .const import DOMAIN
from .sensors_map import SENSOR_MAP
from .value_decoder import decode_value

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Inicjalizacja sensorów SKZP."""
    client = hass.data[DOMAIN]["client"]
    entities = []

    for key, meta in SENSOR_MAP.items():
        if "name" not in meta:
            continue

        # Ustawiamy domyślne wartości, jeśli ich brak w mapie
        meta.setdefault("divider", None)
        meta.setdefault("unit", None)
        meta.setdefault("icon", None)
        meta.setdefault("device_class", None)
        meta.setdefault("state_class", None)

        entity_id = f"sensor.skzp_{meta['name'].lower().replace(' ', '_').replace('.', '')}"
        entities.append(SkzpSensor(client, key, meta, entity_id))

    async_add_entities(entities)
    _LOGGER.info(f"[SKZP] Dodano {len(entities)} sensorów.")


class SkzpSensor(SensorEntity):
    """Encja sensora SKZP."""

    _attr_should_poll = False

    def __init__(self, client, key, meta, entity_id):
        self._client = client
        self._key = key
        
        # ✅ Używamy "native_" - to standard w nowym HA
        self._attr_name = meta.get("name")
        self._attr_unique_id = entity_id
        self._attr_native_unit_of_measurement = meta.get("unit") 
        self._divider = meta.get("divider")
        self._attr_icon = meta.get("icon")
        self.entity_id = entity_id

        if meta.get("state_class"):
            self._attr_state_class = meta["state_class"]
        if meta.get("device_class"):
            self._attr_device_class = meta["device_class"]

        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        
        # Nasłuchujemy zmian danych
        self._remove_listener = self._client.hass.bus.async_listen(
            f"{DOMAIN}_data_update", self._handle_data_update
        )

    @callback
    def _handle_data_update(self, event):
        raw_value = self._client.data.get(self._key)
        
        # Obsługa statusów wirtualnych (Mode, Power, Fan)
        if self._key.startswith("DevStatus_") and raw_value is None:
            raw_value = self._client.data.get("DevStatus", "")
        
        # Dekodowanie wartości tekstowych (np. Alarms)
        decoded = decode_value(self._key, raw_value)

        # Jeśli dekoder zmienił wartość (np. na tekst "Praca"), to ustawiamy i kończymy
        if decoded != str(raw_value):
            self._attr_native_value = decoded
            self.async_write_ha_state()
            return

        if raw_value is None:
            self._attr_native_value = None
            self.async_write_ha_state()
            return

        # ✅ Obsługa liczb i dzielnika
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
        return {
            "identifiers": {(DOMAIN, "skzp_device")},
            "name": "SKZP-02",
            "manufacturer": "Timel",
            "model": "SKZP-02 TCP",
        }