#!/usr/bin/env python3
"""
Test script for HmIP-MP3P (Combination Signalling Device)

Usage:
    cd /Users/lackas/src/hmip
    ~/venv-hmip/bin/python /Users/lackas/src/homematicip-rest-api/scripts/mp3p_test.py [command]

Commands:
    <color> [DIM]   - Set LED color at DIM% brightness (default: 100%)
    off             - Turn off LED
    sound [N] [VOL] - Play sound file N (1-252) at VOL% volume (default: 1, 50%)
    random          - Play random sound
    stop            - Stop sound playback
    status          - Show current device status
    help            - Show this help

Colors: red, green, blue, purple, yellow, white, turquoise

Examples:
    red             - Red at 100%
    blue 50         - Blue at 50%
    sound           - Play sound 001 at 50%
    sound 110       - Play sound 110 at 50%
    sound 110 75    - Play sound 110 at 75%

Colors: BLACK, BLUE, GREEN, TURQUOISE, RED, PURPLE, YELLOW, WHITE

Note: MP3P does NOT support blinking/flashing via API - only static colors.
      Flashing patterns are triggered only through alarm system events.
"""

import asyncio
import sys
import os

# Add the source directory to path for development version
sys.path.insert(0, '/Users/lackas/src/homematicip-rest-api/src')

import homematicip
from homematicip.async_home import AsyncHome
from homematicip.device import CombinationSignallingDevice

# Device ID from your setup
DEVICE_ID = "3014F711A0001522699877CD"


async def get_home():
    """Initialize and return the Home object."""
    config = homematicip.find_and_load_config_file()
    home = AsyncHome()
    await home.init_async(config.access_point, config.auth_token)
    await home.get_current_state_async()
    return home


async def get_device(home: AsyncHome) -> CombinationSignallingDevice:
    """Get the MP3P device."""
    device = home.search_device_by_id(DEVICE_ID)
    if device is None:
        print(f"Device {DEVICE_ID} not found!")
        sys.exit(1)
    return device


async def get_channel(device: CombinationSignallingDevice):
    """Get the notification channel (index 1)."""
    for channel in device.functionalChannels:
        if hasattr(channel, 'set_rgb_dim_level_async'):
            return channel
    print("Notification channel not found!")
    sys.exit(1)


async def show_status(device):
    """Show current device status."""
    print(f"Device: {device.label} ({device.id})")
    print(f"  Type: {device.deviceType}")
    print(f"  Low Battery: {device.lowBat}")
    print(f"  Unreachable: {device.unreach}")

    for ch in device.functionalChannels:
        if hasattr(ch, 'simpleRGBColorState'):
            print(f"\nChannel {ch.index}:")
            print(f"  On: {ch.on}")
            print(f"  Color: {ch.simpleRGBColorState}")
            print(f"  Dim Level: {ch.dimLevel}")
            print(f"  Volume Level: {ch.volumeLevel}")
            print(f"  Sound File: {ch.soundFile}")
            print(f"  Playing: {ch.playingFileActive}")
            print(f"  Optical Signal: {ch.opticalSignalBehaviour}")
            print(f"  MP3 Error State: {ch.mp3ErrorState}")
            print(f"  Profile Mode: {ch.profileMode}")


async def set_color(channel, color: str, dim_level: float = 1.0):
    """Set LED color."""
    print(f"Setting color to {color} at {dim_level*100:.0f}%...")
    result = await channel.set_rgb_dim_level_async(color, dim_level)
    print(f"Result: {result}")


async def play_sound(channel, sound_file: str, volume: float = 0.5):
    """Play a sound file."""
    print(f"Playing {sound_file} at {volume*100:.0f}% volume...")
    result = await channel.set_sound_file_volume_level_async(sound_file, volume)
    print(f"Result: {result}")


async def stop_sound(channel):
    """Stop sound playback."""
    print("Stopping sound...")
    result = await channel.stop_sound_async()
    print(f"Result: {result}")


async def main():
    if len(sys.argv) < 2:
        cmd = "status"
    else:
        cmd = sys.argv[1].lower()

    if cmd == "help":
        print(__doc__)
        return

    home = await get_home()
    device = await get_device(home)
    channel = await get_channel(device)

    # Handle color commands with optional dim level
    colors = ["red", "green", "blue", "purple", "yellow", "white", "turquoise"]
    if cmd in colors:
        dim = 100
        if len(sys.argv) >= 3:
            try:
                dim = int(sys.argv[2])
            except ValueError:
                print(f"Invalid dim level: {sys.argv[2]}")
                sys.exit(1)
        await set_color(channel, cmd.upper(), dim / 100.0)
        return

    # Handle sound command with optional number and volume
    if cmd == "sound":
        sound_num = 1
        volume = 50
        if len(sys.argv) >= 3:
            try:
                sound_num = int(sys.argv[2])
            except ValueError:
                print(f"Invalid sound number: {sys.argv[2]}")
                sys.exit(1)
        if len(sys.argv) >= 4:
            try:
                volume = int(sys.argv[3])
            except ValueError:
                print(f"Invalid volume: {sys.argv[3]}")
                sys.exit(1)
        sound_file = f"SOUNDFILE_{sound_num:03d}"
        await play_sound(channel, sound_file, volume / 100.0)
        return

    commands = {
        "off": lambda: set_color(channel, "BLACK", 0.0),
        "random": lambda: play_sound(channel, "RANDOM_SOUNDFILE", 0.5),
        "stop": lambda: stop_sound(channel),
        "status": lambda: show_status(device),
    }

    if cmd in commands:
        await commands[cmd]()
    else:
        print(f"Unknown command: {cmd}")
        print("Use 'help' for available commands")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
