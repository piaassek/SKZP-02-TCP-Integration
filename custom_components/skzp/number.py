import logging
from homeassistant.components.number import RestoreNumber
from homeassistant.core import callback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# --- UNIWERSALNA MAPA SUWAKÓW (SKZP-02 + SKZP-05) ---
NUMBERS = {
    # ⚙️ WSPÓLNE / SKZP-02
    "BuModulMin": {"name": "Min. modulacja", "min": 1, "max": 100, "step": 1, "icon": "mdi:gauge"},
    "BoilerTempCmd": {"name": "Zad. T. Kotła", "min": 40, "max": 80, "step": 1, "icon": "mdi:thermometer-chevron-up", "divider": 100},
    "DHWTempCmd": {"name": "Zad. T. CWU", "min": 30, "max": 65, "step": 1, "icon": "mdi:water-boiler", "divider": 100},
    "CH1RoomTempCom": {"name": "Temp.Komfort (Stary)", "min": 15, "max": 30, "step": 0.5, "icon": "mdi:home-thermometer", "divider": 100},
    "CH1RoomTempEco": {"name": "Temp. w domu (Eco)", "min": 10, "max": 25, "step": 0.5, "icon": "mdi:leaf", "divider": 100},

    # 📊 NOWE SKZP-05 (Trzy obiegi grzewcze)
    "C030": {"name": "O1 Zad. T. Powrotu", "min": 20, "max": 65, "step": 1, "icon": "mdi:radiator", "divider": 100},
    "C013": {"name": "O1 Temp. Komfortowa", "min": 15, "max": 30, "step": 0.5, "icon": "mdi:home-thermometer", "divider": 100},
    "C014": {"name": "O1 Temp. ECO", "min": 10, "max": 25, "step": 0.5, "icon": "mdi:leaf", "divider": 100},
    "C113": {"name": "O2 Temp. Komfortowa", "min": 15, "max": 30, "step": 0.5, "icon": "mdi:home-thermometer", "divider": 100},
    "C114": {"name": "O2 Temp. ECO", "min": 10, "max": 25, "step": 0.5, "icon": "mdi:leaf", "divider": 100},
    "C213": {"name": "O3 Temp. Komfortowa", "min": 15, "max": 30, "step": 0.5, "icon": "mdi:home-thermometer", "divider": 100},
    "C214": {"name": "O3 Temp. ECO", "min": 10, "max": 25, "step": 0.5, "icon": "mdi:leaf", "divider": 100},
}

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Inicjalizacja suwaków SKZP."""
    client = hass.data[DOMAIN]["client"]
    entities = []
    
    for key, meta in NUMBERS.items():
        entities.append(SkzpNumber(client, key, meta))
        
    async_add_entities(entities)
    _LOGGER.info(f"[SKZP] Dodano {len(entities)} encji sterujących (Number).")


class SkzpNumber(RestoreNumber):
    """Encja reprezentująca parametr do ustawienia w piecu z pamięcią po restarcie."""

    _attr_should_poll = False

    def __init__(self, client, key, meta):
        self._client = client
        self._key = key
        self._meta = meta
        self._attr_name = meta["name"]
        
        self.entity_id = f"number.skzp_{key.lower()}"
        self._attr_unique_id = self.entity_id
        
        self._attr_native_min_value = meta["min"]
        self._attr_native_max_value = meta["max"]
        self._attr_native_step = meta["step"]
        self._attr_icon = meta["icon"]
        
        self._attr_native_value = None 
        self._remove_listener = None

    async def async_added_to_hass(self):
        """Funkcja wywoływana przy dodawaniu encji do HA (np. po restarcie)."""
        await super().async_added_to_hass()
        
        # 1. PANCERNE ZABEZPIECZENIE: Przywracanie ostatniego stanu z bazy danych HA!
        last_number_data = await self.async_get_last_number_data()
        if last_number_data and last_number_data.native_value is not None:
            self._attr_native_value = last_number_data.native_value

        # 2. Podpinamy nasłuchiwanie nowych danych z pieca
        self._remove_listener = self._client.hass.bus.async_listen(
            f"{DOMAIN}_data_update", self._handle_data_update
        )
        # 3. Od razu próbujemy zaktualizować, jeśli piec zdążył już coś wysłać
        self._handle_data_update(None)

    @callback
    def _handle_data_update(self, event):
        """Aktualizacja pozycji suwaka na podstawie danych z pieca."""
        raw_val = self._client.data.get(self._key)
        if raw_val is not None:
            try:
                val = float(raw_val)
                if self._meta.get("divider"):
                    val = val / self._meta["divider"]
                
                # Jeśli nowa wartość z pieca różni się od naszej, zaktualizuj suwak
                if self._attr_native_value != val:
                    self._attr_native_value = val
                    self.async_write_ha_state()
            except ValueError:
                pass

    async def async_set_native_value(self, value: float) -> None:
        """Funkcja wywoływana, gdy przesuniesz suwak w Home Assistant."""
        if self._meta.get("divider"):
            send_val = int(value * self._meta["divider"])
        else:
            send_val = int(value)
            
        # Zapisz natychmiastowo w interfejsie HA
        self._attr_native_value = value
        self.async_write_ha_state()
        
        # Wyślij fizycznie przez TCP do pieca
        await self._client.send_command({self._key: str(send_val)})

    async def async_will_remove_from_hass(self):
        """Sprzątanie przed usunięciem encji z systemu."""
        if self._remove_listener:
            self._remove_listener()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "skzp_device")},
            "name": "SKZP",  # ZMIENIONO NA UNIWERSALNE "SKZP"
            "manufacturer": "Timel",
        }
