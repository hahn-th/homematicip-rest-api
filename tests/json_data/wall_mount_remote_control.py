from tests.json_data.plugable_switch_measuring import fake_home_id

fake_id = 'abc'
fake_id1='def'
fake_id2='ghi'
fake_id3='jkl'
fake_id4='mno'
fake_id5='pqr'
fake_id6='stu'
fake_id7='vwx'
fake_id8='yza'
fake_id9='bcd'

remote_control = {
    'events': {
        '0': {
            'pushEventType': 'DEVICE_CHANGED',
            'device': {
                'id': fake_id,
                'homeId': fake_home_id,
                'label': 'Wall-mount Remote Control',
                'lastStatusUpdate': 1510829714852,
                'type': 'PUSH_BUTTON',
                'functionalChannels': {
                    '0': {
                        'label': '',
                        'deviceId': fake_id,
                        'index': 0,
                        'groupIndex': 0,
                        'functionalChannelType': 'DEVICE_BASE',
                        'groups': [fake_id9],
                        'unreach': False,
                        'lowBat': False,
                        'routerModuleEnabled': False,
                        'routerModuleSupported': False,
                        'rssiDeviceValue': -63,
                        'rssiPeerValue': None
                    },
                    '1': {
                        'label': '',
                        'deviceId': fake_id,
                        'index': 1,
                        'groupIndex': 1,
                        'functionalChannelType': 'SINGLE_KEY_CHANNEL',
                        'groups': [fake_id1, fake_id2]
                    },
                    '2': {
                        'label': '',
                        'deviceId': fake_id,
                        'index': 2,
                        'groupIndex': 1,
                        'functionalChannelType': 'SINGLE_KEY_CHANNEL',
                        'groups': [fake_id1, fake_id2]
                    }
                },
                'oem': 'eQ-3',
                'manufacturerCode': 1,
                'firmwareVersion': '1.4.2',
                'updateState': 'UP_TO_DATE',
                'availableFirmwareVersion': '0.0.0',
                'serializedGlobalTradeItemNumber': fake_id,
                'modelType': 'HMIP-WRC2',
                'modelId': 261
            }
        },
        '1': {
            'pushEventType': 'GROUP_CHANGED',
            'group': {
                'id': fake_id1,
                'homeId': fake_home_id,
                'metaGroupId': None,
                'label': 'Switch',
                'lastStatusUpdate': 1510829714852,
                'unreach': False,
                'lowBat': False,
                'type': 'EXTENDED_LINKED_SWITCHING',
                'channels': [{
                    'deviceId': fake_id,
                    'channelIndex': 2
                }, {
                    'deviceId': fake_id,
                    'channelIndex': 1
                }, {
                    'deviceId': fake_id3,
                    'channelIndex': 1
                }, {
                    'deviceId': fake_id5,
                    'channelIndex': 1
                }],
                'on': False,
                'dimLevel': None,
                'onTime': 111600.0,
                'onLevel': 1.005,
                'sensorSpecificParameters': {
                    '3014F711A00009156993BC67:1': {
                        'type': 'ILLUMINATION',
                        'illuminationDecisionValue': 92
                    }
                }
            }
        },
        '2': {
            'pushEventType': 'GROUP_CHANGED',
            'group': {
                'id': fake_id2,
                'homeId': fake_home_id,
                'metaGroupId': fake_id9,
                'label': 'Living room',
                'lastStatusUpdate': 1510829714852,
                'unreach': False,
                'lowBat': False,
                'type': 'SWITCHING',
                'channels': [{
                    'deviceId': fake_id,
                    'channelIndex': 2
                }, {
                    'deviceId': fake_id,
                    'channelIndex': 1
                }, {
                    'deviceId': fake_id3,
                    'channelIndex': 1
                }, {
                    'deviceId': fake_id5,
                    'channelIndex': 1
                }],
                'on': False,
                'processing': None,
                'dimLevel': None,
                'shutterLevel': None,
                'slatsLevel': None
            }
        },
        '3': {
            'pushEventType': 'GROUP_CHANGED',
            'group': {
                'id': fake_id9,
                'homeId': fake_home_id,
                'metaGroupId': None,
                'label': 'Living room',
                'lastStatusUpdate': 1510829714852,
                'unreach': False,
                'lowBat': False,
                'type': 'META',
                'channels': [{
                    'deviceId': fake_id3,
                    'channelIndex': 0
                }, {
                    'deviceId': fake_id,
                    'channelIndex': 0
                }, {
                    'deviceId': fake_id4,
                    'channelIndex': 0
                }, {
                    'deviceId': fake_id5,
                    'channelIndex': 0
                }, {
                    'deviceId': fake_id6,
                    'channelIndex': 0
                }],
                'groups': [fake_id7, fake_id2, fake_id8]
            }
        }
    },
    'origin': {
        'originType': 'DEVICE',
        'id': fake_id
    }
}