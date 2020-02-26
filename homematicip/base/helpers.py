import codecs
import json
import logging
import re
from datetime import datetime

LOGGER = logging.getLogger(__name__)


def get_functional_channel(channel_type, js):
    for channel in js["functionalChannels"].values():
        if channel["functionalChannelType"] == channel_type:
            return channel
    return None


# from https://bugs.python.org/file43513/json_detect_encoding_3.patch
def detect_encoding(b):
    bstartswith = b.startswith
    if bstartswith((codecs.BOM_UTF32_BE, codecs.BOM_UTF32_LE)):
        return "utf-32"
    if bstartswith((codecs.BOM_UTF16_BE, codecs.BOM_UTF16_LE)):
        return "utf-16"
    if bstartswith(codecs.BOM_UTF8):
        return "utf-8-sig"

    if len(b) >= 4:
        if not b[0]:
            # 00 00 -- -- - utf-32-be
            # 00 XX -- -- - utf-16-be
            return "utf-16-be" if b[1] else "utf-32-be"
        if not b[1]:
            # XX 00 00 00 - utf-32-le
            # XX 00 XX XX - utf-16-le
            return "utf-16-le" if b[2] or b[3] else "utf-32-le"
    elif len(b) == 2:
        if not b[0]:
            # 00 XX - utf-16-be
            return "utf-16-be"
        if not b[1]:
            # XX 00 - utf-16-le
            return "utf-16-le"
    # default
    return "utf-8"


def bytes2str(b):
    if isinstance(b, (bytes, bytearray)):
        return b.decode(detect_encoding(b), "surrogatepass")
    if isinstance(b, str):
        return b
    raise TypeError(
        "the object must be str, bytes or bytearray, not {!r}".format(
            b.__class__.__name__
        )
    )


def handle_config(json_state: str, anonymize: bool) -> str:
    if "errorCode" in json_state:
        LOGGER.error(
            "Could not get the current configuration. Error: %s",
            json_state["errorCode"],
        )
        return None
    else:
        c = json.dumps(json_state, indent=4, sort_keys=True)
        if anonymize:
            # generate dummy guids
            c = anonymizeConfig(
                c,
                "[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
                "00000000-0000-0000-0000-{0:0>12}",
            )
            # generate dummy SGTIN
            c = anonymizeConfig(c, '"[A-Z0-9]{24}"', '"3014F711{0:0>16}"', flags=0)
            # remove refresh Token
            c = anonymizeConfig(c, '"refreshToken": ?"[^"]+"', '"refreshToken": null')
            # location
            c = anonymizeConfig(
                c, '"city": ?"[^"]+"', '"city": "1010, Vienna, Austria"'
            )
            c = anonymizeConfig(c, '"latitude": ?"[^"]+"', '"latitude": "48.208088"')
            c = anonymizeConfig(c, '"longitude": ?"[^"]+"', '"longitude": "16.358608"')

        return c


def anonymizeConfig(config, pattern, format, flags=re.IGNORECASE):
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
