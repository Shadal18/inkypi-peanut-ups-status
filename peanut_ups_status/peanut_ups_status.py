from plugins.base_plugin.base_plugin import BasePlugin
import logging
import requests
from datetime import datetime


logger = logging.getLogger(__name__)


class PeaNUT(BasePlugin):
    def generate_settings_template(self):
        template_params = super().generate_settings_template()
        template_params["style_settings"] = True
        template_params["title"] = {
            "required": False,
            "description": "Custom title for the display",
            "example": "UPS Status",
        }
        template_params["peanut_url"] = {
            "required": True,
            "description": "PeaNUT device API URL",
            "example": "http://docker-host.lan:8080/api/v1/devices/cyberups",
        }
        template_params["show_battery"] = {
            "required": False,
            "description": "Show battery percentage",
        }
        template_params["show_runtime"] = {
            "required": False,
            "description": "Show runtime remaining",
        }
        template_params["show_load"] = {
            "required": False,
            "description": "Show UPS load percentage",
        }
        template_params["show_input_voltage"] = {
            "required": False,
            "description": "Show input voltage",
        }
        template_params["show_output_voltage"] = {
            "required": False,
            "description": "Show output voltage",
        }
        template_params["show_battery_voltage"] = {
            "required": False,
            "description": "Show battery voltage",
        }
        return template_params

    def generate_image(self, settings, device_config):
        title = (settings.get("title") or "").strip() or "UPS Status"
        now_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")

        try:
            raw = self.fetch_peanut_status(settings)
            parsed = self.normalize_status(raw)
        except Exception as e:
            logger.error("Failed to retrieve UPS data: %s", e)
            raise RuntimeError(f"Failed to retrieve UPS data: {e}") from e

        template_params = {
            "title": title,
            "last_refresh_time": now_str,
            "plugin_settings": settings,
            "ups": parsed,
        }

        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        image = self.render_image(
            dimensions,
            "peanut_ups_status.html",
            "peanut_ups_status.css",
            template_params,
        )
        if not image:
            raise RuntimeError("Failed to render UPS status image.")
        return image

    def fetch_peanut_status(self, settings):
        peanut_url = (settings.get("peanut_url") or "").strip()
        if not peanut_url:
            raise RuntimeError("PeaNUT Device URL is required.")

        try:
            response = requests.get(peanut_url, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.Timeout as exc:
            raise RuntimeError("Timed out while querying PeaNUT.") from exc
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"PeaNUT request failed: {exc}") from exc
        except ValueError as exc:
            raise RuntimeError("PeaNUT returned invalid JSON.") from exc

        if isinstance(data, list):
            if not data:
                raise RuntimeError("PeaNUT returned an empty device list.")
            if isinstance(data[0], dict):
                return data[0]

        if isinstance(data, dict) and "ups" in data and isinstance(data["ups"], dict):
            return data["ups"]

        if isinstance(data, dict):
            return data

        raise RuntimeError("Unsupported PeaNUT response format.")

    def normalize_status(self, raw):
        def get_value(*keys, default="—"):
            for key in keys:
                value = raw.get(key)
                if value is not None and str(value).strip() != "":
                    return str(value).strip()
            return default

        def to_float(value):
            try:
                return float(value)
            except Exception:
                return None

        status_code = get_value("ups.status", "status", default="UNKNOWN")
        status_label = self.format_status(status_code)

        battery_charge = get_value("battery.charge", "battery_charge")
        runtime_seconds = get_value("battery.runtime", "battery_runtime")
        ups_load = get_value("ups.load", "load")
        input_voltage = get_value("input.voltage", "input_voltage")
        output_voltage = get_value("output.voltage", "output_voltage")
        battery_voltage = get_value("battery.voltage", "battery_voltage")
        ups_name = get_value("device.model", "ups.model", "model", "name", default="UPS")
        manufacturer = get_value("device.mfr", "ups.mfr", "manufacturer", default="")

        runtime_pretty = self.format_runtime(runtime_seconds)
        battery_pct = self.format_percent(battery_charge)
        load_pct = self.format_percent(ups_load)
        input_v = self.format_voltage(input_voltage)
        output_v = self.format_voltage(output_voltage)
        battery_v = self.format_voltage(battery_voltage)

        battery_numeric = to_float(battery_charge)
        status_class = self.status_class(status_code, battery_numeric)

        return {
            "name": ups_name,
            "manufacturer": manufacturer,
            "status_code": status_code,
            "status_label": status_label,
            "status_class": status_class,
            "battery_pct": battery_pct,
            "runtime_pretty": runtime_pretty,
            "load_pct": load_pct,
            "input_v": input_v,
            "output_v": output_v,
            "battery_v": battery_v,
        }

    def format_status(self, code):
        code = (code or "").upper()
        if "OB" in code:
            if "LB" in code:
                return "On Battery (Low)"
            return "On Battery"
        if "OL" in code:
            return "Online"
        if "CHRG" in code:
            return "Charging"
        if "DISCHRG" in code:
            return "Discharging"
        if "BYPASS" in code:
            return "Bypass"
        return code or "Unknown"

    def status_class(self, code, battery_numeric):
        code = (code or "").upper()
        if "LB" in code:
            return "danger"
        if "OB" in code:
            return "warning"
        if battery_numeric is not None and battery_numeric <= 25:
            return "warning"
        return "good"

    def format_percent(self, value):
        try:
            return f"{round(float(value))}%"
        except Exception:
            return "—"

    def format_voltage(self, value):
        try:
            return f"{float(value):.1f} V"
        except Exception:
            return "—"

    def format_runtime(self, seconds):
        try:
            seconds = int(float(seconds))
            if seconds < 0:
                return "—"
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            if hours > 0:
                return f"{hours}h {minutes}m"
            return f"{minutes}m"
        except Exception:
            return "—"