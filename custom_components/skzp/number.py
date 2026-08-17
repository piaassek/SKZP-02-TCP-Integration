import logging
from homeassistant.components.number import RestoreNumber
from homeassistant.core import callback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# --- DEFINICJE SUWAKÓW ---
COMMON_NUMBERS = {
    "BoilerTempCmd": {"name": "Zadana temp. kotła", "min": 40, "max": 80, "step": 1, "icon": "mdi:thermometer-chevron-up", "divider": 100},
    "DHWTempCmd": {"name": "Zadana temp. CWU", "min": 30, "max": 65, "step": 1, "icon": "mdi:water-boiler", "divider": 100},
    "BuModulMin": {"name": "Min. modulacja", "min": 1, "max": 100, "step": 1, "icon": "mdi:gauge"},
    "BuModulMax": {"name": "Maks. modulacja", "min": 1, "max": 100, "step": 1, "icon": "mdi:gauge-full"},
}

SKZP02_NUMBERS = {
    "CH1RoomTempCom": {"name": "Temp. komfortowa", "min": 15, "max": 30, "step": 0.5, "icon": "mdi:home-thermometer", "divider": 100},
    "CH1RoomTempEco": {"name": "Temp. ECO", "min": 10, "max": 25, "step": 0.5, "icon": "mdi:leaf", "divider": 100},
    "CH1ReturnTempCmd": {"name": "Zadana temp. powrotu", "min": 20, "max": 65, "step": 1, "icon": "mdi:radiator", "divider": 100},
    "CH1MixTempCmd": {"name": "Zadana temp. mieszacza", "min": 20, "max": 70, "step": 1, "icon": "mdi:valve", "divider": 100},
}

SKZP05_CIRCUITS = {
    "C0": {
        "C030": {"name": "Obieg 1: Zadana temp. powrotu", "min": 20, "max": 65, "step": 1, "icon": "mdi:radiator", "divider": 100},
        "C013": {"name": "Obieg 1: Temp. komfortowa", "min": 15, "max": 30, "step": 0.5, "icon": "mdi:home-thermometer", "divider": 100},
        "C014": {"name": "Obieg 1: Temp. ECO", "min": 10, "max": 25, "step": 0.5, "icon": "mdi:leaf", "divider": 100},
        "C027": {"name": "Obieg 1: Maks. temp. mieszacza", "min": 20, "max": 70, "step": 1, "icon": "mdi:thermometer-chevron-up", "divider": 100},
    },
    "C1": {
        "C113": {"name": "Obieg 2: Temp. komfortowa", "min": 15, "max": 30, "step": 0.5, "icon": "mdi:home-thermometer", "divider": 100},
        "C114": {"name": "Obieg 2: Temp. ECO", "min": 10, "max": 25, "step": 0.5, "icon": "mdi:leaf", "divider": 100},
        "C127": {"name": "Obieg 2: Maks. temp. mieszacza", "min": 20, "max": 70, "step": 1, "icon": "mdi:thermometer-chevron-up", "divider": 100},
    },
    "C2": {
        "C213": {"name": "Obieg 3: Temp. komfortowa", "min": 15, "max": 30, "step": 0.5, "icon": "mdi:home-thermometer", "divider": 100},
        "C214": {"name": "Obieg 3: Temp. ECO", "min": 10, "max": 25, "step": 0.5, "icon": "mdi:leaf", "divider": 100},
        "C227": {"name": "Obieg 3: Maks. temp. mieszacza", "min": 20, "max": 70, "step": 1, "icon": "mdi:thermometer-chevron-up", "divider": 100},
    },
}

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Inicjalizacja suwaków SKZP zależnie od wykrytego modelu."""
    client = hass.data[DOMAIN][config_entry.entry_id]
    entry_id = config_entry.entry_id
    entities = []
    
    # Wspólne dla obu modeli
    for key, meta in COMMON_NUMBERS.items():
        entities.append(SkzpNumber(client, entry_id, key, meta))
        
    # Dobór suwaków specyficznych dla modelu
    if client.is_skzp05:
        for prefix, circuit_numbers in SKZP05_CIRCUITS.items():
            has_circuit = any(k in client.data for k in circuit_numbers.keys())
            if has_circuit:
                for key, meta in circuit_numbers.items():
                    if key in client.data:
                        entities.append(SkzpNumber(client, entry_id, key, meta))
    else:
        for key, meta in SKZP02_NUMBERS.items():
            entities.append(SkzpNumber(client, entry_id, key, meta))
        
    async_add_entities(entities)
    _LOGGER.info(f"[SKZP] Dodano {len(entities)} encji sterujących (Number) dla modelu {'SKZP-05' if client.is_skzp05 else 'SKZP-02'}.")



class SkzpNumber(RestoreNumber):
    """Encja reprezentująca parametr do ustawienia w piecu z pamięcią po restarcie."""

    _attr_should_poll = False

    def __init__(self, client, entry_id, key, meta):
        self._client = client
        self._key = key
        self._meta = meta
        self._attr_name = meta["name"]
        self._attr_unique_id = f"{entry_id}_{key.lower()}"
        
        self._attr_native_min_value = meta["min"]
        self._attr_native_max_value = meta["max"]
        self._attr_native_step = meta["step"]
        self._attr_icon = meta["icon"]

        
        self._attr_native_value = None 
        self._remove_listener = None

    async def async_added_to_hass(self):
        """Funkcja wywoływana przy dodawaniu encji do HA (np. po restarcie)."""
        await super().async_added_to_hass()
        
        # 1. Przywracanie ostatniego stanu z bazy danych HA
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
                    self._attr_native_value = round(val, 2)
                    self.async_write_ha_state()
            except ValueError:
                pass

    async def async_set_native_value(self, value: float) -> None:
        """Funkcja wywoływana, gdy przesuniesz suwak w Home Assistant."""
        if self._meta.get("divider"):
            send_val = int(round(value * self._meta["divider"]))
        else:
            send_val = int(round(value))
            
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
        dev_type = self._client.data.get("DevType", "SKZP")
        model = "SKZP-05" if "05" in str(dev_type) else ("SKZP-02" if "02" in str(dev_type) else "SKZP")
        return {
            "identifiers": {(DOMAIN, "skzp_device")},
            "name": f"Sterownik {model}",
            "manufacturer": "Timel",
            "model": str(dev_type),
        }


