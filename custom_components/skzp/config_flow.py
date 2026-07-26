import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from .const import DOMAIN, DEFAULT_HOST, DEFAULT_PORT

class SkzpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Prosty config flow dla SKZP."""

    VERSION = 1

    async def async_step_import(self, import_info):
        """Obsługa importu z configuration.yaml."""
        host = import_info.get("host", DEFAULT_HOST)
        port = import_info.get("port", DEFAULT_PORT)

        # Sprawdź, czy integracja już istnieje
        for entry in self._async_current_entries():
            if entry.data.get("host") == host and entry.data.get("port") == port:
                return self.async_abort(reason="already_configured")

        return self.async_create_entry(title="SKZP YAML", data={"host": host, "port": port})

    async def async_step_user(self, user_input=None):
        """Ręczna konfiguracja przez GUI (opcjonalna)."""
        if user_input is not None:
            return self.async_create_entry(title="SKZP", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
            }
        )
        return self.async_show_form(step_id="user", data_schema=data_schema)
