fake_device_id = '4014G711N50021D569B5804B'
fake_home_id = '7b3ae3bb-be04-34d4-7af8-aa706570e0af'

plugable_switch_measuring = {
    'id': fake_device_id,
    'homeId': fake_home_id,
    'label': 'Pluggable Switch and Meter',
    'lastStatusUpdate': 1510564962120,
    'type': 'PLUGABLE_SWITCH_MEASURING',
    'functionalChannels':
        {'0':
             {'label': '',
              'deviceId': fake_device_id,
              'index': 0,
              'groupIndex': 0,
              'functionalChannelType': 'DEVICE_BASE',
              'groups': [
                  '8ba14126-6403-4f75-9c0f-1950e7d7563a'],
              'unreach': False,
              'lowBat': None,
              'routerModuleEnabled': False,
              'routerModuleSupported': True,
              'rssiDeviceValue': -52,
              'rssiPeerValue': -48},
         '1': {'label': '',
               'deviceId': fake_device_id,
               'index': 1,
               'groupIndex': 1,
               'functionalChannelType': 'SWITCH_MEASURING_CHANNEL',
               'groups': [
                   'f71c7f28-5ce1-44a8-845f-aed0a8337e68',
                   'f5218c3d-05e4-4260-9c37-c336d882967e'],
               'on': False,
               'profileMode': 'AUTOMATIC',
               'userDesiredProfileMode': 'AUTOMATIC',
               'energyCounter': 0.0002,
               'currentPowerConsumption': 0.0}},
    'oem': 'eQ-3', 'manufacturerCode': 1,
    'firmwareVersion': '2.6.2',
    'updateState': 'UP_TO_DATE',
    'availableFirmwareVersion': '2.6.2',
    'serializedGlobalTradeItemNumber': fake_device_id,
    'modelType': 'HMIP-PSM', 'modelId': 262}
