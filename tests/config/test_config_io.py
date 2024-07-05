from unittest.mock import patch, mock_open

from homematicip.configuration.config_io import ConfigIO


def test_get_output_format_config_without_existing_config_file():
    with patch("os.path.exists", return_value=False):
        output_format_config = ConfigIO.get_output_format_config()
        assert output_format_config is not None


def test_get_output_format_config_with_existing_config_file():
    format_file_content = r'''
{
    "device_attributes": ["id", "label", "modelType"],
    "group_attributes": ["id", "label"],
    "functional_channel_attributes": ["id", "label", "functionalChannelType"]
}
    '''
    mock_data = mock_open(read_data=format_file_content)
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_data):
            output_format_config = ConfigIO.get_output_format_config()
            assert output_format_config is not None
            assert output_format_config.device_attributes == ["id", "label", "modelType"]
            assert output_format_config.group_attributes == ["id", "label"]
            assert output_format_config.functional_channel_attributes == ["id", "label", "functionalChannelType"]
