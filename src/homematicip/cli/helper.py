import click

from homematicip.model import Model
from homematicip.model.devices import Device
from homematicip.model.functional_channels import FunctionalChannel


def get_rssi_bar_string(rssi_value):
    """Create a bar string for the rssi value."""
    # Observed values: -93..-47
    width = 10
    dots = 0
    if rssi_value:
        dots = int(round((100 + rssi_value) / 5))
        dots = max(0, min(width, dots))

    return "[{}{}]".format("*" * dots, "_" * (width - dots))


def get_channel_by_index_of_first(device: Device, index: int = None) -> FunctionalChannel | None:
    """Get the first channel of a device or the channel with the given index."""
    if index is not None:
        if str(index) not in device.functionalChannels:
            raise click.BadParameter(f"Channel {index} not found for device {device.label or device.id} (.")

        return device.functionalChannels[str(index)]

    click.echo("No channel index given. Use first channel.")
    return device.functionalChannels["1"]
