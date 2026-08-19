import asyncio
import json
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry
from homeassistant.config_entries import SOURCE_IMPORT

from .const import DOMAIN, DEFAULT_HOST, DEFAULT_PORT, CONF_PIN, DEFAULT_PIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "binary_sensor", "number", "select"]


async def async_setup(hass: HomeAssistant, config: ConfigType):
    """Utwórz wpis integracji z YAML jeśli nie istnieje."""
    hass.data.setdefault(DOMAIN, {})

    if DOMAIN in config:
        host = config[DOMAIN].get("host", DEFAULT_HOST)
        port = config[DOMAIN].get("port", DEFAULT_PORT)
        pin = config[DOMAIN].get(CONF_PIN, DEFAULT_PIN)

        existing_entries = hass.config_entries.async_entries(DOMAIN)
        if not existing_entries:
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    DOMAIN,
                    context={"source": SOURCE_IMPORT},
                    data={"host": host, "port": port, CONF_PIN: pin},
                )
            )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Konfiguracja po utworzeniu wpisu konfiguracyjnego."""
    host = entry.data.get("host", DEFAULT_HOST)
    port = entry.data.get("port", DEFAULT_PORT)
    pin = entry.data.get(CONF_PIN, DEFAULT_PIN)

    skzp_client = SkzpTcpClient(hass, host, port, pin)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = skzp_client
    await skzp_client.start()

    # Czekamy krótko na pierwszą ramkę danych (np. do 5s), aby wykryć model sterownika (SKZP-02 vs SKZP-05)
    await skzp_client.wait_for_data(timeout=5.0)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Wyładowanie integracji."""
    client: "SkzpTcpClient" = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    if client:
        await client.stop()
        
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)



class SkzpTcpClient:
    """Prosty klient TCP odbierający linie JSON (ASCII) i publikujący eventy w HA."""

    def __init__(self, hass: HomeAssistant, host: str, port: int, pin: str = DEFAULT_PIN):
        self.hass = hass
        self.host = host
        self.port = port
        self.pin = str(pin)
        self._reader = None
        self._writer = None
        self._task: asyncio.Task | None = None
        self.data: dict = {}
        self._connected = False
        self._first_data_event = asyncio.Event()

    @property
    def is_skzp05(self) -> bool:
        dev_type = str(self.data.get("DevType", ""))
        return "05" in dev_type or "C030" in self.data or "C006" in self.data

    @property
    def is_skzp02(self) -> bool:
        dev_type = str(self.data.get("DevType", ""))
        return "02" in dev_type or "CH1MixTempAct" in self.data or not self.is_skzp05

    async def wait_for_data(self, timeout: float = 5.0):
        """Oczekuje na pierwszą poprawną ramkę danych."""
        try:
            await asyncio.wait_for(self._first_data_event.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            pass

    async def start(self):
        self._task = asyncio.create_task(self._read_loop())


    async def stop(self):
        if self._writer:
            try:
                self._writer.close()
                await self._writer.wait_closed()
            except Exception:
                pass
            self._writer = None
            self._reader = None
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except Exception:
                pass

    async def _reconnect(self):
        _LOGGER.warning("[SKZP] Utracono połączenie — próba ponownego połączenia za 5s...")
        self._connected = False
        if self._writer:
            try:
                self._writer.close()
                await self._writer.wait_closed()
            except Exception:
                pass
            self._writer = None
            self._reader = None
        await asyncio.sleep(5)
        await self._connect()

    async def _connect(self):
        while True:
            try:
                _LOGGER.info(f"[SKZP] Łączenie z bramką {self.host}:{self.port}...")
                self._reader, self._writer = await asyncio.wait_for(
                    asyncio.open_connection(self.host, self.port), timeout=10.0
                )
                self._connected = True
                _LOGGER.info(f"[SKZP] Połączono pomyślnie z {self.host}:{self.port}")
                return
            except asyncio.CancelledError:
                raise
            except Exception as e:
                _LOGGER.warning(f"[SKZP] Błąd połączenia z {self.host}:{self.port}: {e} — ponawiam za 5s")
                await asyncio.sleep(5)

    async def _read_loop(self):
        await self._connect()
        buffer = ""
        while True:
            try:
                chunk = await asyncio.wait_for(self._reader.read(4096), timeout=60)
                if not chunk:
                    _LOGGER.warning("[SKZP] Połączenie zamknięte przez bramkę — wznawianie...")
                    await self._reconnect()
                    continue

                buffer += chunk.decode("utf-8", errors="ignore")

                # Wyodrębnianie kompletnych obiektów JSON {...} ze strumienia
                while "{" in buffer and "}" in buffer:
                    start = buffer.find("{")
                    end = buffer.find("}", start)
                    if end == -1:
                        # Obcięty JSON — czekamy na kolejną paczkę danych
                        buffer = buffer[start:]
                        break

                    json_str = buffer[start : end + 1]
                    buffer = buffer[end + 1 :]

                    try:
                        parsed = json.loads(json_str)
                        if isinstance(parsed, dict):
                            self.data.update(parsed)
                            self._first_data_event.set()
                            _LOGGER.debug(f"[SKZP] Odebrano dane ({len(parsed)} pól)")
                            self.hass.bus.async_fire(f"{DOMAIN}_data_update")
                    except Exception as e:
                        _LOGGER.debug(f"[SKZP] Błąd parsowania wycinka JSON: {e}")

            except asyncio.TimeoutError:
                _LOGGER.warning("[SKZP] Brak danych przez 60s — odświeżam połączenie")
                await self._reconnect()
            except asyncio.CancelledError:
                break
            except Exception as e:
                _LOGGER.error(f"[SKZP] Błąd w pętli odbioru: {e}")
                await self._reconnect()


    async def send_command(self, parameters: dict):
        """Wysyła komendę do pieca."""
        if not self._connected or not self._writer:
            _LOGGER.error("[SKZP] Brak połączenia, nie można wysłać komendy.")
            return

        # Pobieramy dynamicznie Token, DevId i DevPin z ostatnich odebranych danych
        dev_id = self.data.get("DevId", "APLSI")
        token = self.data.get("Token", "MOZHW")
        dev_pin = self.data.get("DevPin", self.pin) if self.pin == DEFAULT_PIN else self.pin

        # Budowa ramki autoryzacyjnej
        payload = {
            "DevId": dev_id,
            "DevPin": dev_pin,
            "Token": token
        }

        # Dodajemy nasze parametry do zmiany
        payload.update(parameters)

        # Zamieniamy na tekst i dodajemy znak nowej linii (\n)
        command_str = json.dumps(payload) + "\n"
        
        try:
            self._writer.write(command_str.encode('utf-8'))
            await self._writer.drain()
            _LOGGER.info(f"[SKZP] Sukces! Wysłano komendę: {command_str.strip()}")
        except Exception as e:
            _LOGGER.error(f"[SKZP] Błąd wysyłania komendy: {e}")