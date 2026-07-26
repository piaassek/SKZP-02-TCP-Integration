import logging
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.core import callback

from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)

# 🔸 Mapa binarnych sygnałów z DevStatus
# indeks = pozycja w surowym stringu DevStatus
PUMP_KEYS = {
    "DevStatus_Podajnik": ("Podajnik", 9),
    "DevStatus_CO1": ("Pompa CO1", 10),
    "DevStatus_CO2": ("Pompa CO2", 11),
    "DevStatus_CWU": ("Pompa CWU", 12),
    "DevStatus_CWR": ("Pompa CWR", 13),
    "DevStatus_CO3": ("Pompa CO3", 14),
    "DevStatus_COB": ("Pompa COB", 15),
}

async def async_setup_entry(hass, config_entry, async_add_entities):
    client = hass.data[DOMAIN]["client"]
    entities = [
        DevStatusBinarySensor(client, key, name, index)
        for key, (name, index) in PUMP_KEYS.items()
    ]
    async_add_entities(entities)
    _LOGGER.info(f"[SKZP] Dodano {len(entities)} binary sensorów z DevStatus.")


class DevStatusBinarySensor(BinarySensorEntity):
    """Binarne sensory statusu pomp i podajnika."""

    _attr_should_poll = False

    def __init__(self, client, key, name, index):
        self._client = client
        self._key = key
        self._index = index
        self._attr_name = name
        self.entity_id = f"binary_sensor.skzp_{key.lower()}"
        self._attr_unique_id = self.entity_id  # 👈 DODAJ TO
        self._remove_listener = self._client.hass.bus.async_listen(
            f"{DOMAIN}_data_update", self._handle_data_update
        )
        self._attr_is_on = False


    @callback
    def _handle_data_update(self, event):
        devstatus = self._client.data.get("DevStatus", "")
        if len(devstatus) > self._index:
            self._attr_is_on = devstatus[self._index] == "1"
        else:
            self._attr_is_on = False
        self.async_write_ha_state()

    async def async_will_remove_from_hass(self):
        if self._remove_listener:
            self._remove_listener()

    @property
    def device_info(self):
        """Powiązanie sensora z urządzeniem SKZP."""
        return {
            "identifiers": {(DOMAIN, "skzp_device")},
            "name": "SKZP-02T",
            "manufacturer": "SKZP",
            "model": "SKZP TCP Integration",
        }
