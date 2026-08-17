import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from .const import DOMAIN, DEFAULT_HOST, DEFAULT_PORT, CONF_PIN, DEFAULT_PIN


class SkzpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow dla integracji SKZP."""

    VERSION = 1

    async def async_step_import(self, import_info):
        """Obsługa importu z configuration.yaml."""
        host = import_info.get("host", DEFAULT_HOST)
        port = import_info.get("port", DEFAULT_PORT)
        pin = import_info.get(CONF_PIN, DEFAULT_PIN)

        await self.async_set_unique_id(f"{host}:{port}")
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"SKZP ({host})",
            data={"host": host, "port": port, CONF_PIN: pin}
        )

    async def async_step_user(self, user_input=None):
        """Konfiguracja przez interfejs użytkownika."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]

            await self.async_set_unique_id(f"{host}:{port}")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"SKZP ({host})",
                data=user_input
            )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
                vol.Required(CONF_PIN, default=DEFAULT_PIN): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
