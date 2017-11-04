import logging

_LOGGER = logging.getLogger(__name__)


class HmipIpObject:
    on_update = None

    def update(self):
        """trigger the method tied to on_update."""
        if self.on_update is not None:
            self.on_update()
        else:
            _LOGGER.debug(
                'on_update event not fired as has no method is assigned to it.')
