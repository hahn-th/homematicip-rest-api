"""Default execution entry point if running the package via python -m."""
import sys

import homematicip.cli.hmip_cli


def main():
    """Run pypyr from script entry point."""
    return homematicip.cli.hmip_cli.main()


if __name__ == '__main__':
    sys.exit(main())
