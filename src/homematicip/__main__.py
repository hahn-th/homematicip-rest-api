"""Default execution entry point if running the package via python -m."""
import homematicip.cli.hmip_cli
import sys


def main():
    """Run pypyr from script entry point."""
    return homematicip.cli.hmip_cli.main()


if __name__ == '__main__':
    sys.exit(main())