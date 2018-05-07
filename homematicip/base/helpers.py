from datetime import datetime
import codecs

def get_functional_channel(channel_type, js):
    for channel in js['functionalChannels'].values():
        if channel['functionalChannelType'] == channel_type:
            return channel
    return None

#from https://bugs.python.org/file43513/json_detect_encoding_3.patch
def detect_encoding(b):
    bstartswith = b.startswith
    if bstartswith((codecs.BOM_UTF32_BE, codecs.BOM_UTF32_LE)):
        return 'utf-32'
    if bstartswith((codecs.BOM_UTF16_BE, codecs.BOM_UTF16_LE)):
        return 'utf-16'
    if bstartswith(codecs.BOM_UTF8):
        return 'utf-8-sig'

    if len(b) >= 4:
        if not b[0]:
            # 00 00 -- -- - utf-32-be
            # 00 XX -- -- - utf-16-be
            return 'utf-16-be' if b[1] else 'utf-32-be'
        if not b[1]:
            # XX 00 00 00 - utf-32-le
            # XX 00 XX XX - utf-16-le
            return 'utf-16-le' if b[2] or b[3] else 'utf-32-le'
    elif len(b) == 2:
        if not b[0]:
            # 00 XX - utf-16-be
            return 'utf-16-be'
        if not b[1]:
            # XX 00 - utf-16-le
            return 'utf-16-le'
    # default
    return 'utf-8'

def bytes2str(b):
    if isinstance(b,(bytes,bytearray)):
        return b.decode(detect_encoding(b), 'surrogatepass')
    if isinstance(b, str):
        return b
    raise TypeError('the object must be str, bytes or bytearray, not {!r}'.format(b.__class__.__name__))