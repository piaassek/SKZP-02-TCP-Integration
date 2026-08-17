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
    hass.data[DOMAIN]["client"] = skzp_client
    await skzp_client.start()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Wyładowanie integracji."""
    client: "SkzpTcpClient" = hass.data[DOMAIN].get("client")
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
                self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
                self._connected = True
                _LOGGER.info(f"[SKZP] Połączono z {self.host}:{self.port}")
                return
            except Exception as e:
                _LOGGER.error(f"[SKZP] Błąd połączenia: {e} — ponawiam za 10s")
                await asyncio.sleep(10)

    async def _read_loop(self):
        await self._connect()
        buffer = b""
        while True:
            try:
                # timeout chroni przed wiszeniem gdy urządzenie milczy
                line = await asyncio.wait_for(self._reader.readline(), timeout=60)
                if not line:
                    await self._reconnect()
                    continue

                # zdarzają się fragmenty — sklejaj do pełnej linii JSON
                buffer += line
                if not buffer.rstrip().endswith(b"}"):
                    continue

                line_str = buffer.decode(errors="ignore").strip()
                buffer = b""  # czyścimy bufor po pełnej ramce

                if line_str.startswith("{") and line_str.endswith("}"):
                    try:
                        parsed = json.loads(line_str)
                        # aktualizujemy słownik danych
                        self.data.update(parsed)

                        # publikujemy event dla sensorów/binary_sensorów
                        self.hass.bus.async_fire(f"{DOMAIN}_data_update")
                    except Exception as e:
                        _LOGGER.warning(f"[SKZP] Błąd parsowania JSON: {e}; ramka='{line_str[:200]}'")
                else:
                    _LOGGER.debug(f"[SKZP] Pominięto niepełną/niepoprawną ramkę: {line_str[:200]}")

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

        # Pobieramy dynamicznie Token i DevId z ostatnich odebranych danych
        dev_id = self.data.get("DevId", "APLSI")
        token = self.data.get("Token", "MOZHW")

        # Budowa ramki autoryzacyjnej
        payload = {
            "DevId": dev_id,
            "DevPin": self.pin,
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