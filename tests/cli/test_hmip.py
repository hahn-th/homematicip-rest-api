from click.testing import CliRunner

from homematicip.cli import hmip

#
# def test_version():
#     result = CliRunner().invoke(hmip.cli, ["version"])
#     assert result.exit_code == 0
#     assert "HomematicIP-Rest-Api" in result.output
#
# def test_list_devices(mocker):
#     result = CliRunner().invoke(hmip.cli, ["list", "devices"])
#     assert result.exit_code == 0
