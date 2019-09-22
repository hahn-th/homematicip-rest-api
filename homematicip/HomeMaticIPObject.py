from homematicip.base.HomeMaticIPObject import HomeMaticIPObject
import warnings, logging

LOGGER = logging.getLogger(__name__)

LOGGER.warning(
    DeprecationWarning(
        "homematicip.HomeMaticIPObject is deprecated in favor of homematicip.base.HomeMaticIPObject"
    )
)
