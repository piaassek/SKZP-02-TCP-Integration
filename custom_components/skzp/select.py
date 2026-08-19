import asyncio
import logging
import time
from homeassistant.components.select import SelectEntity
from homeassistant.core import callback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Mapa: Ładna nazwa w HA -> Komenda do pieca
DHW_MODES = {
    "Wyłączona": "Stop",
    "Auto": "Still_On", 
    "Timer": "Timer",
    "Ciągła praca": "PumpStillOn"
}

DHW_MODES_INV = {v: k for k, v in DHW_MODES.items()}

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Inicjalizacja listy wyboru dla SKZP."""
    client = hass.data[DOMAIN][config_entry.entry_id]
    entry_id = config_entry.entry_id
    async_add_entities([SkzpDHWModeSelect(client, entry_id)])
    _LOGGER.info("[SKZP] Dodano encję select (Tryb CWU).")

class SkzpDHWModeSelect(SelectEntity):
    """Encja listy rozwijanej dla trybu pompy CWU."""

    _attr_should_poll = False
    _attr_name = "Tryb pompy CWU"
    _attr_icon = "mdi:water-pump"

    def __init__(self, client, entry_id):
        self._client = client
        self._attr_unique_id = f"{entry_id}_dhwmode"
        self._attr_options = list(DHW_MODES.keys())
        self._attr_current_option = None
        self._remove_listener = None
        self._pending_target = None
        self._pending_until = None

    async def async_added_to_hass(self):
        """Nasłuchiwanie po restarcie."""
        self._remove_listener = self._client.hass.bus.async_listen(
            f"{DOMAIN}_data_update", self._handle_data_update
        )
        self._handle_data_update(None)

    @callback
    def _handle_data_update(self, event):
        """Aktualizacja wybranej opcji na podstawie danych z pieca."""
        raw_val = self._client.data.get("DHWMode")
        if raw_val in DHW_MODES_INV:
            new_val = DHW_MODES_INV[raw_val]

            # Zabezpieczenie przed cofaniem wyboru przez starą ramkę
            if self._pending_until is not None:
                now = time.time()
                if now < self._pending_until:
                    if new_val == self._pending_target:
                        self._pending_until = None
                        self._pending_target = None
                    else:
                        return
                else:
                    self._pending_until = None
                    self._pending_target = None

            if self._attr_current_option != new_val:
                self._attr_current_option = new_val
                self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        """Wysyłanie wybranej opcji do pieca."""
        if option in DHW_MODES:
            val_to_send = DHW_MODES[option]
            
            # Zmiana wizualna w UI i blokada starych ramek
            self._attr_current_option = option
            self._pending_target = option
            self._pending_until = time.time() + 3.0
            self.async_write_ha_state()
            
            # Wysłanie komendy JSON przez TCP
            await self._client.send_command({"DHWMode": val_to_send})




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
