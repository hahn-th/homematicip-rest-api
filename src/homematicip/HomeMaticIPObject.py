import logging
import warnings

from homematicip.base.homematicip_object import HomeMaticIPObject

LOGGER = logging.getLogger(__name__)

LOGGER.warning(
    DeprecationWarning(
        "homematicip.HomeMaticIPObject is deprecated in favor of homematicip.base.HomeMaticIPObject"
    )
)
