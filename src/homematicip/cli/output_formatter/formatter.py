from homematicip.configuration.output_format_config import OutputFormatConfig
from homematicip.model.model_components import FunctionalChannel


def generate_output_functional_channel(fc: FunctionalChannel, output_format_config: OutputFormatConfig) -> str:
    """Generate a string representation of a FunctionalChannel object based on the output format configuration."""
    return _generate_output(fc, output_format_config.functional_channel_attributes)


def generate_output_group(group, output_format_config: OutputFormatConfig) -> str:
    """Generate a string representation of a Group object based on the output format configuration."""
    return _generate_output(group, output_format_config.group_attributes)


def generate_output_device(device, output_format_config: OutputFormatConfig) -> str:
    """Generate a string representation of a Device object based on the output format configuration."""
    return _generate_output(device, output_format_config.device_attributes)

def _generate_output(group, attributes):
    outputs = []

    for attrib_name in attributes:
        if hasattr(group, attrib_name):
            outputs.append(f"{attrib_name}: {getattr(group, attrib_name)}")

    return ", ".join(outputs)