import logging
import re

LOGGER = logging.getLogger(__name__)


def handle_config(config_string: str, anonymize: bool) -> str:
    if anonymize:
        # generate dummy guids
        config_string = _anonymize_config(
            config_string,
            "[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
            "00000000-0000-0000-0000-{0:0>12}",
        )
        # generate dummy SGTIN
        config_string = _anonymize_config(config_string, '"[A-Z0-9]{24}"', '"3014F711{0:0>16}"', flags=0)
        # remove refresh Token
        config_string = _anonymize_config(config_string, '"refreshToken": ?"[^"]+"', '"refreshToken": null')
        # location
        config_string = _anonymize_config(
            config_string, '"city": ?"[^"]+"', '"city": "1010, Vienna, Austria"'
        )
        config_string = _anonymize_config(config_string, '"latitude": ?"[^"]+"', '"latitude": "48.208088"')
        config_string = _anonymize_config(config_string, '"longitude": ?"[^"]+"', '"longitude": "16.358608"')

    return config_string


def _anonymize_config(config, pattern, format, flags=re.IGNORECASE):
    m = re.findall(pattern, config, flags=flags)
    if m is None:
        return config
    map = {}
    i = 0
    for s in m:
        if s in map.keys():
            continue
        map[s] = format.format(i)
        i = i + 1

    for k, v in map.items():
        config = config.replace(k, v)
    return config
