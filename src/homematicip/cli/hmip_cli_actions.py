# from homematicip.model import Model
#
#
# def handle_list_devices(model: Model):
#     print("Devices:")
#     for device in sorted(model.devices.values(), key=lambda x: x.label):
#         print(f"\t{device.id}\t{device.label}\t{device.type}")
#
#     return True
#
# def handle_list_groups(model: Model):
#     print("Groups:")
#     for group in sorted(model.groups.values(), key=lambda x: x.label):
#         print(f"\t{group.id}\t{group.label}\t{group.type}")
#
#     return True
#
# def handle_list_last_status_update(model: Model):
#     print("Devices:")
#     for device in sorted(model.devices.values(), key=lambda x: x.label):
#         print(f"\t{device.id}\t{device.label}\t{device.lastStatusUpdate}")
#
#     print("Groups:")
#     for group in sorted(model.groups.values(), key=lambda x: x.label):
#         print(f"\t{group.id}\t{group.label}\t{group.lastStatusUpdate}")
#
#     return True
#
# def handle_list_group_ids(model: Model):
#     for g in sorted(model.groups.values(), key=lambda x: x.label):
#         print("Id: {} - Type: {} - Label: {}".format(g.id, g.type, g.label))
#     return True
#
import click

from homematicip.model import Model


def handle_list_rssi(model: Model):
    click.echo(
        "{:45s} - Duty cycle: {:2}".format(
            "HmIP AccessPoint",
            model.home.dutyCycle if model.home.dutyCycle is not None else "None",
        )
    )

    for d in sorted(model.devices.values(), key=lambda x: x.label):
        fc = d.functionalChannels["0"]
        rssi_device_value = 0
        rssi_peer_value = 0
        unreach = False

        if hasattr(fc, "rssiDeviceValue"):
            rssi_device_value = fc.rssiDeviceValue
        if hasattr(fc, "rssiPeerValue"):
            rssi_peer_value = fc.rssiPeerValue
        if hasattr(fc, "unreach"):
            unreach = fc.unreach
        click.echo(
            "{:45s} - RSSI: {:4} {} - Peer RSSI: {:4} - {} {} permanentlyReachable: {}".format(
                d.label,
                rssi_device_value if rssi_device_value else 0,
                get_rssi_bar_string(rssi_device_value),
                rssi_peer_value if rssi_peer_value else 0,
                get_rssi_bar_string(rssi_peer_value),
                "Unreachable" if unreach else "",
                d.permanentlyReachable,
            )
        )
    return True


def get_rssi_bar_string(rssi_value):
    """Create a bar string for the rssi value."""
    # Observed values: -93..-47
    width = 10
    dots = 0
    if rssi_value:
        dots = int(round((100 + rssi_value) / 5))
        dots = max(0, min(width, dots))

    return "[{}{}]".format("*" * dots, "_" * (width - dots))
