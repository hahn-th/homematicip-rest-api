from datetime import datetime


def get_functional_channel(channel_type, js):
    for channel in js['functionalChannels'].values():
        if channel['functionalChannelType'] == channel_type:
            return channel
    return None