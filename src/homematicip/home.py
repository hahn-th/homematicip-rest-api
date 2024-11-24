from homematicip.async_home import AsyncHome
from homematicip.group import *
from homematicip.securityEvent import *

LOGGER = logging.getLogger(__name__)


class Home(AsyncHome):
    """this class represents the 'Home' of the homematic ip"""

    def activate_absence_permanent(self):
        return self._run_non_async(self.activate_absence_permanent_async)

    def activate_absence_with_duration(self, duration: int):
        return self._run_non_async(self.activate_absence_with_duration_async, duration)

    def activate_absence_with_period(self, endtime: datetime):
        return self._run_non_async(self.activate_absence_with_period_async, endtime)

    def activate_vacation(self, endtime: datetime, temperature: float):
        return self._run_non_async(self.activate_vacation_async, endtime, temperature)

    def deactivate_absence(self):
        return self._run_non_async(self.deactivate_absence_async)

    def deactivate_vacation(self):
        return self._run_non_async(self.deactivate_vacation_async)

    def download_configuration(self) -> dict:
        return self._run_non_async(self.download_configuration_async)

    def get_current_state(self, clear_config: bool = False) -> dict:
        return self._run_non_async(self.get_current_state_async, clear_config)

    def get_OAuth_OTK(self):
        return self._run_non_async(self.get_OAuth_OTK_async)

    def get_security_journal(self):
        return self._run_non_async(self.get_security_journal_async)

    def set_cooling(self, cooling):
        return self._run_non_async(self.set_cooling_async, cooling)

    def set_intrusion_alert_through_smoke_detectors(self, activate: bool = True):
        return self._run_non_async(self.set_intrusion_alert_through_smoke_detectors_async, activate)

    def set_location(self, city, latitude, longitude):
        return self._run_non_async(self.set_location_async, city, latitude, longitude)

    def set_pin(self, newPin: str, oldPin: str = None) -> dict:
        return self._run_non_async(self.set_pin_async, newPin, oldPin)

    def set_powermeter_unit_price(self, price):
        return self._run_non_async(self.set_powermeter_unit_price_async, price)

    def set_security_zones_activation(self, internal=True, external=True):
        return self._run_non_async(self.set_security_zones_activation_async, internal, external)

    def set_silent_alarm(self, internal=True, external=True):
        return self._run_non_async(self.set_silent_alarm_async, internal, external)

    def set_timezone(self, timezone: str):
        return self._run_non_async(self.set_timezone_async, timezone)

    def set_zone_activation_delay(self, delay):
        return self._run_non_async(self.set_zone_activation_delay_async, delay)

    def start_inclusion(self, deviceId):
        return self._run_non_async(self.start_inclusion_async, deviceId)

    def set_zones_device_assignment(self, internal_devices, external_devices):
        return self._run_non_async(self.set_zones_device_assignment_async, internal_devices, external_devices)
