import logging
import warnings

from homematicip.base.HomeMaticIPObject import HomeMaticIPObject

LOGGER = logging.getLogger(__name__)

LOGGER.warning(
    DeprecationWarning(
        "homematicip.HomeMaticIPObject is deprecated in favor of homematicip.base.HomeMaticIPObject"
    )
)
