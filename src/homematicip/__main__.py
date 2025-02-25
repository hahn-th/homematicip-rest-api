"""Default execution entry point if running the package via python -m."""
import asyncio
import sys

import homematicip.cli.hmip_cli


def main():
    """Run pypyr from script entry point."""
    return asyncio.run(homematicip.cli.hmip_cli.main_async())


if __name__ == '__main__':
    sys.exit(main())
