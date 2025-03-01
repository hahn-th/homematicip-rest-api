import locale
import platform


class ClientCharacteristicsBuilder:

    @staticmethod
    def _get_lang() -> str:
        """Determines the language."""
        def_locale = locale.getlocale()
        if def_locale is not None and def_locale[0] is not None:
            return def_locale[0]

        return "en_US"

    @classmethod
    def get(cls, access_point_id: str) -> dict:
        """Return client characteristics as dictionary
        :param access_point_id: The access point id
        :return: The client characteristics as dictionary"""

        return {
            "clientCharacteristics": {
                "apiVersion": "10",
                "applicationIdentifier": "homematicip-python",
                "applicationVersion": "1.0",
                "deviceManufacturer": "none",
                "deviceType": "Computer",
                "language": cls._get_lang(),
                "osType": platform.system(),
                "osVersion": platform.release(),
            },
            "id": access_point_id,
        }
