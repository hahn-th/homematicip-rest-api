current_state = {
    'home': {
        'weather': {
            'temperature': 11.0,
            'weatherCondition': 'HEAVILY_CLOUDY',
            'weatherDayTime': 'DAY',
            'minTemperature': 11.0,
            'maxTemperature': 11.0,
            'humidity': 81,
            'windSpeed': 18.36,
            'windDirection': 240
        },
        'metaGroups': ['8ba14126-6403-4f75-9c0f-1950e7d7563a',
                       'ec4cb9d5-70e1-4b3f-9e26-14fe979fb265'],
        'clients': ['9a7ccb90-fe7a-47a5-8bb7-f11b7c78b5ef',
                    '594bbe72-1ce9-441f-87d8-138b7e94b1de',
                    '4a69ad10-bd93-4a88-bf1f-422cdaea2f7b',
                    'a28d2f18-4aa9-4ce4-8a7d-18ea585c9fb3'],
        'connected': True,
        'currentAPVersion': '1.2.2',
        'availableAPVersion': None,
        'timeZoneId': 'CET',
        'location': {
            'city': ' Nijmegen, Netherlands',
            'latitude': '51.8125626',
            'longitude': '5.8372264'
        },
        'pinAssigned': False,
        'dutyCycle': 0.5,
        'updateState': 'UP_TO_DATE',
        'powerMeterUnitPrice': 0.0,
        'powerMeterCurrency': 'EUR',
        'deviceUpdateStrategy': 'MANUALLY',
        'lastReadyForUpdateTimestamp': 1498712798641,
        'functionalHomes': {
            'INDOOR_CLIMATE': {
                'functionalGroups': ['7c166920-e1dc-4e76-9e1b-5dac0abb02d3',
                                     'f3ad2f07-1b5d-4233-8c41-04af7a878a66'],
                'absenceType': 'NOT_ABSENT',
                'absenceEndTime': None,
                'floorHeatingSpecificGroups': {
                    'HEATING_TEMPERATURE_LIMITER': '84972276-92b4-41b0-9b9f-b8c10c243789',
                    'HEATING_DEHUMIDIFIER': '64a3d164-9f98-4dd7-8d4f-6f671b7c0451',
                    'HEATING_CHANGEOVER': '1f596432-372b-4267-829b-741ca7d0e802',
                    'HEATING_HUMIDITY_LIMITER': '4fec6f97-7921-44bd-a372-4d007e8eea2b',
                    'HEATING_EXTERNAL_CLOCK': 'b0c83172-1263-4591-8260-1d4f69d0f88f',
                    'HEATING_COOLING_DEMAND_BOILER': 'c92821f0-6f38-4d79-8e9c-7d74b2350787',
                    'HEATING_COOLING_DEMAND_PUMP': '82bcaa28-bf09-4131-9ae1-8b830f74c08a'
                },
                'ecoTemperature': 17.0,
                'coolingEnabled': False,
                'ecoDuration': 'PERMANENT',
                'solution': 'INDOOR_CLIMATE',
                'active': True
            },
            'LIGHT_AND_SHADOW': {
                'functionalGroups': ['cc4c1ac1-a881-41d4-b0e6-de4266b67f08'],
                'extendedLinkedSwitchingGroups': [
                    '46ee7f5b-e3de-4182-9b95-c42fda52492e'],
                'extendedLinkedShutterGroups': [],
                'switchingProfileGroups': [
                    '74793b85-8245-40c4-bfe0-1e99b8009fb0'],
                'shutterProfileGroups': [],
                'solution': 'LIGHT_AND_SHADOW',
                'active': True
            },
            'SECURITY_AND_ALARM': {
                'functionalGroups': ['21c53d30-f686-407b-847b-fa74f8980dfc'],
                'alarmEventTimestamp': None,
                'alarmEventDeviceId': None,
                'alarmSecurityJournalEntryType': None,
                'alarmActive': False,
                'securityZones': {
                    'EXTERNAL': '64ff862e-26eb-4880-8644-fb3e9f70836e',
                    'INTERNAL': '0709ebb4-c030-4ffb-b49b-365cd0ef950d'
                },
                'securitySwitchingGroups': {
                    'SIREN': 'f2bc6ab0-2cfc-4538-a945-7f4887d1b8a6',
                    'PANIC': '6a4846e2-9357-45d9-9f5c-eddd29b0490b',
                    'ALARM': 'd0b1430e-bfe6-4b57-a78e-f98767d2b652',
                    'COMING_HOME': '14a8ab48-3929-4408-9a70-66eeed48d44f'
                },
                'zoneActivationDelay': 0.0,
                'intrusionAlertThroughSmokeDetectors': False,
                'solution': 'SECURITY_AND_ALARM',
                'activationInProgress': False,
                'active': True
            }
        },
        'inboxGroup': '783b0268-24d6-4607-995a-ff2172dfc17b',
        'apExchangeClientId': None,
        'apExchangeState': 'NONE',
        'voiceControlSettings': {
            'allowedActiveSecurityZoneIds': []
        },
        'ruleGroups': [],
        'id': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf'
    },
    'groups': {
        '4fec6f97-7921-44bd-a372-4d007e8eea2b': {
            'id': '4fec6f97-7921-44bd-a372-4d007e8eea2b',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'HEATING_HUMIDITY_LIMITER',
            'lastStatusUpdate': 0,
            'unreach': None,
            'lowBat': None,
            'type': 'HEATING_HUMIDITY_LIMITER',
            'channels': []
        },
        '46ee7f5b-e3de-4182-9b95-c42fda52492e': {
            'id': '46ee7f5b-e3de-4182-9b95-c42fda52492e',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'Night light',
            'lastStatusUpdate': 1509618648274,
            'unreach': False,
            'lowBat': False,
            'type': 'EXTENDED_LINKED_SWITCHING',
            'channels': [{
                'deviceId': '3014F711A0000193C99517FF',
                'channelIndex': 2
            }, {
                'deviceId': '3014F711A0000193C99517FF',
                'channelIndex': 1
            }, {
                'deviceId': '3014F711A00001D569A5804B',
                'channelIndex': 1
            }],
            'on': False,
            'dimLevel': None,
            'onTime': 111600.0,
            'onLevel': 1.005,
            'sensorSpecificParameters': {}
        },
        '64ff862e-26eb-4880-8644-fb3e9f70836e': {
            'id': '64ff862e-26eb-4880-8644-fb3e9f70836e',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'EXTERNAL',
            'lastStatusUpdate': 1509617225429,
            'unreach': False,
            'lowBat': False,
            'type': 'SECURITY_ZONE',
            'channels': [{
                'deviceId': '3014F711A00000D569A4A7AE',
                'channelIndex': 1
            }, {
                'deviceId': '3014F711A00000D569A4A7AE',
                'channelIndex': 0
            }],
            'active': False,
            'silent': False,
            'ignorableDevices': [],
            'windowState': 'CLOSED',
            'motionDetected': None,
            'presenceDetected': None,
            'sabotage': False
        },
        '1f596432-372b-4267-829b-741ca7d0e802': {
            'id': '1f596432-372b-4267-829b-741ca7d0e802',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'HEATING_CHANGEOVER',
            'lastStatusUpdate': 0,
            'unreach': None,
            'lowBat': None,
            'type': 'HEATING_CHANGEOVER',
            'channels': [],
            'on': None,
            'dimLevel': None
        },
        '64a3d164-9f98-4dd7-8d4f-6f671b7c0451': {
            'id': '64a3d164-9f98-4dd7-8d4f-6f671b7c0451',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'HEATING_DEHUMIDIFIER',
            'lastStatusUpdate': 0,
            'unreach': None,
            'lowBat': None,
            'type': 'HEATING_DEHUMIDIFIER',
            'channels': [],
            'on': None,
            'dimLevel': None
        },
        '21c53d30-f686-407b-847b-fa74f8980dfc': {
            'id': '21c53d30-f686-407b-847b-fa74f8980dfc',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': '8ba14126-6403-4f75-9c0f-1950e7d7563a',
            'label': 'Living room',
            'lastStatusUpdate': 1509617225429,
            'unreach': False,
            'lowBat': False,
            'type': 'SECURITY',
            'channels': [{
                'deviceId': '3014F711A00000D569A4A7AE',
                'channelIndex': 1
            }],
            'windowState': 'CLOSED',
            'motionDetected': None,
            'presenceDetected': None,
            'sabotage': False,
            'smokeDetectorAlarmType': None
        },
        '74793b85-8245-40c4-bfe0-1e99b8009fb0': {
            'id': '74793b85-8245-40c4-bfe0-1e99b8009fb0',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'Test',
            'lastStatusUpdate': 1509617158261,
            'unreach': False,
            'lowBat': None,
            'type': 'SWITCHING_PROFILE',
            'channels': [{
                'deviceId': '3014F711A00001D569A5804B',
                'channelIndex': 1
            }],
            'on': False,
            'dimLevel': None,
            'profileId': '70afd748-d7e2-4859-b5a0-867930d4eca4',
            'profileMode': 'AUTOMATIC'
        },
        'f2bc6ab0-2cfc-4538-a945-7f4887d1b8a6': {
            'id': 'f2bc6ab0-2cfc-4538-a945-7f4887d1b8a6',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'SIREN',
            'lastStatusUpdate': 0,
            'unreach': None,
            'lowBat': None,
            'type': 'ALARM_SWITCHING',
            'channels': [],
            'on': None,
            'dimLevel': None,
            'onTime': 180.0,
            'signalAcoustic': 'FREQUENCY_RISING',
            'signalOptical': 'DOUBLE_FLASHING_REPEATING',
            'smokeDetectorAlarmType': None,
            'acousticFeedbackEnabled': True
        },
        'f3ad2f07-1b5d-4233-8c41-04af7a878a66': {
            'id': 'f3ad2f07-1b5d-4233-8c41-04af7a878a66',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': '8ba14126-6403-4f75-9c0f-1950e7d7563a',
            'label': 'Living room',
            'lastStatusUpdate': 1509617225429,
            'unreach': False,
            'lowBat': False,
            'type': 'HEATING',
            'channels': [{
                'deviceId': '3014F711A00000D569A4A7AE',
                'channelIndex': 1
            }],
            'windowOpenTemperature': 12.0,
            'setPointTemperature': None,
            'minTemperature': 5.0,
            'maxTemperature': 30.0,
            'windowState': 'CLOSED',
            'cooling': None,
            'partyMode': False,
            'controlMode': 'AUTOMATIC',
            'profiles': {
                'PROFILE_3': {
                    'profileId': '2b7e35b7-4d94-4470-bc52-0484476afc8a',
                    'groupId': 'f3ad2f07-1b5d-4233-8c41-04af7a878a66',
                    'index': 'PROFILE_3',
                    'name': '',
                    'visible': False,
                    'enabled': True
                },
                'PROFILE_6': {
                    'profileId': 'bb86737c-bdf0-45f8-b9b3-cf80e3a82c2a',
                    'groupId': 'f3ad2f07-1b5d-4233-8c41-04af7a878a66',
                    'index': 'PROFILE_6',
                    'name': '',
                    'visible': False,
                    'enabled': False
                },
                'PROFILE_5': {
                    'profileId': '32d0f391-a207-46fb-b562-70e7d610cd40',
                    'groupId': 'f3ad2f07-1b5d-4233-8c41-04af7a878a66',
                    'index': 'PROFILE_5',
                    'name': '',
                    'visible': False,
                    'enabled': False
                },
                'PROFILE_4': {
                    'profileId': '66b91be9-4f88-469c-8b20-c7c4a3fec8c8',
                    'groupId': 'f3ad2f07-1b5d-4233-8c41-04af7a878a66',
                    'index': 'PROFILE_4',
                    'name': '',
                    'visible': True,
                    'enabled': False
                },
                'PROFILE_1': {
                    'profileId': '02926003-adfe-4a60-904e-1b7f5ea31437',
                    'groupId': 'f3ad2f07-1b5d-4233-8c41-04af7a878a66',
                    'index': 'PROFILE_1',
                    'name': '',
                    'visible': True,
                    'enabled': True
                },
                'PROFILE_2': {
                    'profileId': '25e16472-92d7-4e85-93b9-6b428235303e',
                    'groupId': 'f3ad2f07-1b5d-4233-8c41-04af7a878a66',
                    'index': 'PROFILE_2',
                    'name': '',
                    'visible': False,
                    'enabled': True
                }
            },
            'activeProfile': 'PROFILE_1',
            'boostMode': False,
            'boostDuration': 5,
            'actualTemperature': None,
            'humidity': None,
            'coolingAllowed': True,
            'coolingIgnored': False,
            'ecoAllowed': True,
            'ecoIgnored': False,
            'controllable': False,
            'floorHeatingMode': 'FLOOR_HEATING_STANDARD',
            'humidityLimitEnabled': True,
            'humidityLimitValue': 60,
            'externalClockEnabled': False,
            'externalClockHeatingTemperature': 19.0,
            'externalClockCoolingTemperature': 23.0
        },
        'ec4cb9d5-70e1-4b3f-9e26-14fe979fb265': {
            'id': 'ec4cb9d5-70e1-4b3f-9e26-14fe979fb265',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'Bedroom',
            'lastStatusUpdate': 1509619396810,
            'unreach': False,
            'lowBat': False,
            'type': 'META',
            'channels': [{
                'deviceId': '3014F711A0000393C99A1282',
                'channelIndex': 0
            }],
            'groups': ['7c166920-e1dc-4e76-9e1b-5dac0abb02d3']
        },
        'c92821f0-6f38-4d79-8e9c-7d74b2350787': {
            'id': 'c92821f0-6f38-4d79-8e9c-7d74b2350787',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'HEATING_COOLING_DEMAND_BOILER',
            'lastStatusUpdate': 0,
            'unreach': None,
            'lowBat': None,
            'type': 'HEATING_COOLING_DEMAND_BOILER',
            'channels': [],
            'on': None,
            'dimLevel': None,
            'boilerLeadTime': 0,
            'boilerFollowUpTime': 0
        },
        '6a4846e2-9357-45d9-9f5c-eddd29b0490b': {
            'id': '6a4846e2-9357-45d9-9f5c-eddd29b0490b',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'PANIC',
            'lastStatusUpdate': 0,
            'unreach': None,
            'lowBat': None,
            'type': 'LINKED_SWITCHING',
            'channels': [],
            'on': None,
            'dimLevel': None
        },
        'd0b1430e-bfe6-4b57-a78e-f98767d2b652': {
            'id': 'd0b1430e-bfe6-4b57-a78e-f98767d2b652',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'ALARM',
            'lastStatusUpdate': 0,
            'unreach': None,
            'lowBat': None,
            'type': 'ALARM_SWITCHING',
            'channels': [],
            'on': None,
            'dimLevel': None,
            'onTime': 7200.0,
            'signalAcoustic': 'FREQUENCY_RISING',
            'signalOptical': 'DOUBLE_FLASHING_REPEATING',
            'smokeDetectorAlarmType': None,
            'acousticFeedbackEnabled': True
        },
        '783b0268-24d6-4607-995a-ff2172dfc17b': {
            'id': '783b0268-24d6-4607-995a-ff2172dfc17b',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'INBOX',
            'lastStatusUpdate': 0,
            'unreach': None,
            'lowBat': None,
            'type': 'INBOX',
            'channels': []
        },
        '0709ebb4-c030-4ffb-b49b-365cd0ef950d': {
            'id': '0709ebb4-c030-4ffb-b49b-365cd0ef950d',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'INTERNAL',
            'lastStatusUpdate': 0,
            'unreach': None,
            'lowBat': None,
            'type': 'SECURITY_ZONE',
            'channels': [],
            'active': False,
            'silent': False,
            'ignorableDevices': [],
            'windowState': None,
            'motionDetected': None,
            'presenceDetected': None,
            'sabotage': None
        },
        '7c166920-e1dc-4e76-9e1b-5dac0abb02d3': {
            'id': '7c166920-e1dc-4e76-9e1b-5dac0abb02d3',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': 'ec4cb9d5-70e1-4b3f-9e26-14fe979fb265',
            'label': 'Bedroom',
            'lastStatusUpdate': 1509619396810,
            'unreach': False,
            'lowBat': False,
            'type': 'HEATING',
            'channels': [{
                'deviceId': '3014F711A0000393C99A1282',
                'channelIndex': 1
            }],
            'windowOpenTemperature': 12.0,
            'setPointTemperature': 25.0,
            'minTemperature': 5.0,
            'maxTemperature': 30.0,
            'windowState': None,
            'cooling': None,
            'partyMode': False,
            'controlMode': 'MANUAL',
            'profiles': {
                'PROFILE_4': {
                    'profileId': '532401a4-9eed-4f52-8233-4156539c0f67',
                    'groupId': '7c166920-e1dc-4e76-9e1b-5dac0abb02d3',
                    'index': 'PROFILE_4',
                    'name': '',
                    'visible': True,
                    'enabled': False
                },
                'PROFILE_3': {
                    'profileId': 'c7467785-7eaf-44b1-8d18-bc1a138e6607',
                    'groupId': '7c166920-e1dc-4e76-9e1b-5dac0abb02d3',
                    'index': 'PROFILE_3',
                    'name': '',
                    'visible': False,
                    'enabled': True
                },
                'PROFILE_6': {
                    'profileId': '7cbd55aa-b882-4dfe-a6c0-a6d28837625f',
                    'groupId': '7c166920-e1dc-4e76-9e1b-5dac0abb02d3',
                    'index': 'PROFILE_6',
                    'name': '',
                    'visible': False,
                    'enabled': False
                },
                'PROFILE_1': {
                    'profileId': '9a86570d-b4ff-4772-9f2c-642112419177',
                    'groupId': '7c166920-e1dc-4e76-9e1b-5dac0abb02d3',
                    'index': 'PROFILE_1',
                    'name': '',
                    'visible': True,
                    'enabled': True
                },
                'PROFILE_5': {
                    'profileId': 'eb6237ab-6c6c-4528-b8bf-95c4bd7192f2',
                    'groupId': '7c166920-e1dc-4e76-9e1b-5dac0abb02d3',
                    'index': 'PROFILE_5',
                    'name': '',
                    'visible': False,
                    'enabled': False
                },
                'PROFILE_2': {
                    'profileId': 'cc56d1eb-f686-4046-953a-e24cc523cd9d',
                    'groupId': '7c166920-e1dc-4e76-9e1b-5dac0abb02d3',
                    'index': 'PROFILE_2',
                    'name': '',
                    'visible': False,
                    'enabled': True
                }
            },
            'activeProfile': 'PROFILE_1',
            'boostMode': False,
            'boostDuration': 5,
            'actualTemperature': None,
            'humidity': None,
            'coolingAllowed': False,
            'coolingIgnored': False,
            'ecoAllowed': True,
            'ecoIgnored': False,
            'controllable': True,
            'floorHeatingMode': 'FLOOR_HEATING_STANDARD',
            'humidityLimitEnabled': True,
            'humidityLimitValue': 60,
            'externalClockEnabled': False,
            'externalClockHeatingTemperature': 19.0,
            'externalClockCoolingTemperature': 23.0
        },
        '84972276-92b4-41b0-9b9f-b8c10c243789': {
            'id': '84972276-92b4-41b0-9b9f-b8c10c243789',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'HEATING_TEMPERATURE_LIMITER',
            'lastStatusUpdate': 0,
            'unreach': None,
            'lowBat': None,
            'type': 'HEATING_TEMPERATURE_LIMITER',
            'channels': []
        },
        'cc4c1ac1-a881-41d4-b0e6-de4266b67f08': {
            'id': 'cc4c1ac1-a881-41d4-b0e6-de4266b67f08',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': '8ba14126-6403-4f75-9c0f-1950e7d7563a',
            'label': 'Living room',
            'lastStatusUpdate': 1509618648274,
            'unreach': False,
            'lowBat': False,
            'type': 'SWITCHING',
            'channels': [{
                'deviceId': '3014F711A0000193C99517FF',
                'channelIndex': 2
            }, {
                'deviceId': '3014F711A0000193C99517FF',
                'channelIndex': 1
            }, {
                'deviceId': '3014F711A00001D569A5804B',
                'channelIndex': 1
            }],
            'on': False,
            'processing': None,
            'dimLevel': None,
            'shutterLevel': None,
            'slatsLevel': None
        },
        '82bcaa28-bf09-4131-9ae1-8b830f74c08a': {
            'id': '82bcaa28-bf09-4131-9ae1-8b830f74c08a',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'HEATING_COOLING_DEMAND_PUMP',
            'lastStatusUpdate': 0,
            'unreach': None,
            'lowBat': None,
            'type': 'HEATING_COOLING_DEMAND_PUMP',
            'channels': [],
            'on': None,
            'dimLevel': None,
            'pumpLeadTime': 2,
            'pumpFollowUpTime': 2,
            'pumpProtectionDuration': 1,
            'pumpProtectionSwitchingInterval': 14
        },
        '8ba14126-6403-4f75-9c0f-1950e7d7563a': {
            'id': '8ba14126-6403-4f75-9c0f-1950e7d7563a',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'Living room',
            'lastStatusUpdate': 1509618648274,
            'unreach': False,
            'lowBat': False,
            'type': 'META',
            'channels': [{
                'deviceId': '3014F711A0000193C99517FF',
                'channelIndex': 0
            }, {
                'deviceId': '3014F711A00001D569A5804B',
                'channelIndex': 0
            }, {
                'deviceId': '3014F711A00000D569A4A7AE',
                'channelIndex': 0
            }],
            'groups': ['21c53d30-f686-407b-847b-fa74f8980dfc',
                       'cc4c1ac1-a881-41d4-b0e6-de4266b67f08',
                       'f3ad2f07-1b5d-4233-8c41-04af7a878a66']
        },
        '14a8ab48-3929-4408-9a70-66eeed48d44f': {
            'id': '14a8ab48-3929-4408-9a70-66eeed48d44f',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'COMING_HOME',
            'lastStatusUpdate': 1509617158261,
            'unreach': False,
            'lowBat': None,
            'type': 'LINKED_SWITCHING',
            'channels': [{
                'deviceId': '3014F711A00001D569A5804B',
                'channelIndex': 1
            }],
            'on': False,
            'dimLevel': None
        },
        'b0c83172-1263-4591-8260-1d4f69d0f88f': {
            'id': 'b0c83172-1263-4591-8260-1d4f69d0f88f',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'metaGroupId': None,
            'label': 'HEATING_EXTERNAL_CLOCK',
            'lastStatusUpdate': 0,
            'unreach': None,
            'lowBat': None,
            'type': 'HEATING_EXTERNAL_CLOCK',
            'channels': []
        }
    },
    'devices': {
        '3014F711A0000193C99517FF': {
            'id': '3014F711A0000193C99517FF',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'label': 'Wall-mount Remote Control',
            'lastStatusUpdate': 1509618648274,
            'type': 'PUSH_BUTTON',
            'functionalChannels': {
                '0': {
                    'label': '',
                    'deviceId': '3014F711A0000193C99517FF',
                    'index': 0,
                    'groupIndex': 0,
                    'functionalChannelType': 'DEVICE_BASE',
                    'groups': ['8ba14126-6403-4f75-9c0f-1950e7d7563a'],
                    'unreach': False,
                    'lowBat': False,
                    'routerModuleEnabled': False,
                    'routerModuleSupported': False
                },
                '1': {
                    'label': '',
                    'deviceId': '3014F711A0000193C99517FF',
                    'index': 1,
                    'groupIndex': 1,
                    'functionalChannelType': 'SINGLE_KEY_CHANNEL',
                    'groups': ['46ee7f5b-e3de-4182-9b95-c42fda52492e',
                               'cc4c1ac1-a881-41d4-b0e6-de4266b67f08']
                },
                '2': {
                    'label': '',
                    'deviceId': '3014F711A0000193C99517FF',
                    'index': 2,
                    'groupIndex': 1,
                    'functionalChannelType': 'SINGLE_KEY_CHANNEL',
                    'groups': ['46ee7f5b-e3de-4182-9b95-c42fda52492e',
                               'cc4c1ac1-a881-41d4-b0e6-de4266b67f08']
                }
            },
            'updateState': 'UP_TO_DATE',
            'firmwareVersion': '1.4.2',
            'availableFirmwareVersion': '1.4.2'
        },
        '3014F711A0000393C99A1282': {
            'id': '3014F711A0000393C99A1282',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'label': 'Radiator Thermostat',
            'lastStatusUpdate': 1509619396810,
            'type': 'HEATING_THERMOSTAT',
            'functionalChannels': {
                '0': {
                    'label': '',
                    'deviceId': '3014F711A0000393C99A1282',
                    'index': 0,
                    'groupIndex': 0,
                    'functionalChannelType': 'DEVICE_OPERATIONLOCK',
                    'groups': ['ec4cb9d5-70e1-4b3f-9e26-14fe979fb265'],
                    'unreach': False,
                    'lowBat': False,
                    'routerModuleEnabled': False,
                    'routerModuleSupported': False,
                    'operationLockActive': False
                },
                '1': {
                    'label': '',
                    'deviceId': '3014F711A0000393C99A1282',
                    'index': 1,
                    'groupIndex': 1,
                    'functionalChannelType': 'HEATING_THERMOSTAT_CHANNEL',
                    'groups': ['7c166920-e1dc-4e76-9e1b-5dac0abb02d3'],
                    'temperatureOffset': 0.0,
                    'valvePosition': 1.0
                }
            },
            'updateState': 'UP_TO_DATE',
            'firmwareVersion': '1.6.3',
            'availableFirmwareVersion': '1.6.3'
        },
        '3014F711A00001D569A5804B': {
            'id': '3014F711A00001D569A5804B',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'label': 'Pluggable Switch and Meter',
            'lastStatusUpdate': 1509617158261,
            'type': 'PLUGABLE_SWITCH_MEASURING',
            'functionalChannels': {
                '0': {
                    'label': '',
                    'deviceId': '3014F711A00001D569A5804B',
                    'index': 0,
                    'groupIndex': 0,
                    'functionalChannelType': 'DEVICE_BASE',
                    'groups': ['8ba14126-6403-4f75-9c0f-1950e7d7563a'],
                    'unreach': False,
                    'lowBat': None,
                    'routerModuleEnabled': False,
                    'routerModuleSupported': True
                },
                '1': {
                    'label': '',
                    'deviceId': '3014F711A00001D569A5804B',
                    'index': 1,
                    'groupIndex': 1,
                    'functionalChannelType': 'SWITCH_MEASURING_CHANNEL',
                    'groups': ['46ee7f5b-e3de-4182-9b95-c42fda52492e',
                               '74793b85-8245-40c4-bfe0-1e99b8009fb0',
                               'cc4c1ac1-a881-41d4-b0e6-de4266b67f08',
                               '14a8ab48-3929-4408-9a70-66eeed48d44f'],
                    'on': False,
                    'profileMode': 'AUTOMATIC',
                    'userDesiredProfileMode': 'AUTOMATIC',
                    'energyCounter': 0.0002,
                    'currentPowerConsumption': 0.0
                }
            },
            'updateState': 'UP_TO_DATE',
            'firmwareVersion': '2.6.2',
            'availableFirmwareVersion': '2.6.2'
        },
        '3014F711A00000D569A4A7AE': {
            'id': '3014F711A00000D569A4A7AE',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'label': 'Window / Door Contact',
            'lastStatusUpdate': 1509617225429,
            'type': 'SHUTTER_CONTACT',
            'functionalChannels': {
                '0': {
                    'label': '',
                    'deviceId': '3014F711A00000D569A4A7AE',
                    'index': 0,
                    'groupIndex': 0,
                    'functionalChannelType': 'DEVICE_SABOTAGE',
                    'groups': ['64ff862e-26eb-4880-8644-fb3e9f70836e',
                               '8ba14126-6403-4f75-9c0f-1950e7d7563a'],
                    'unreach': False,
                    'lowBat': False,
                    'routerModuleEnabled': False,
                    'routerModuleSupported': False,
                    'sabotage': False
                },
                '1': {
                    'label': '',
                    'deviceId': '3014F711A00000D569A4A7AE',
                    'index': 1,
                    'groupIndex': 1,
                    'functionalChannelType': 'SHUTTER_CONTACT_CHANNEL',
                    'groups': ['64ff862e-26eb-4880-8644-fb3e9f70836e',
                               '21c53d30-f686-407b-847b-fa74f8980dfc',
                               'f3ad2f07-1b5d-4233-8c41-04af7a878a66'],
                    'windowState': 'CLOSED',
                    'eventDelay': 0
                }
            },
            'updateState': 'UP_TO_DATE',
            'firmwareVersion': '1.12.2',
            'availableFirmwareVersion': '1.12.2'
        }
    },
    'clients': {
        '9a7ccb90-fe7a-47a5-8bb7-f11b7c78b5ef': {
            'id': '9a7ccb90-fe7a-47a5-8bb7-f11b7c78b5ef',
            'label': 'ONEPLUS A3003',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'refreshToken': None
        },
        '594bbe72-1ce9-441f-87d8-138b7e94b1de': {
            'id': '594bbe72-1ce9-441f-87d8-138b7e94b1de',
            'label': 'SM-T800',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'refreshToken': None
        },
        '4a69ad10-bd93-4a88-bf1f-422cdaea2f7b': {
            'id': '4a69ad10-bd93-4a88-bf1f-422cdaea2f7b',
            'label': 'homematicip-python',
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'refreshToken': None
        },
        'a28d2f18-4aa9-4ce4-8a7d-18ea585c9fb3': {
            'id': 'a28d2f18-4aa9-4ce4-8a7d-18ea585c9fb3',
            'label': "Sander's iPad",
            'homeId': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf',
            'refreshToken': None
        }
    }
}

incoming_event = {
    'events': {
        '0': {
            'pushEventType': 'HOME_CHANGED',
            'home': {
                'weather': {
                    'temperature': 11.0,
                    'weatherCondition': 'HEAVILY_CLOUDY',
                    'weatherDayTime': 'DAY',
                    'minTemperature': 11.0,
                    'maxTemperature': 11.0,
                    'humidity': 81,
                    'windSpeed': 18.36,
                    'windDirection': 240
                },
                'metaGroups': ['8ba14126-6403-4f75-9c0f-1950e7d7563a',
                               'ec4cb9d5-70e1-4b3f-9e26-14fe979fb265'],
                'clients': ['9a7ccb90-fe7a-47a5-8bb7-f11b7c78b5ef',
                            '594bbe72-1ce9-441f-87d8-138b7e94b1de',
                            '4a69ad10-bd93-4a88-bf1f-422cdaea2f7b',
                            'a28d2f18-4aa9-4ce4-8a7d-18ea585c9fb3'],
                'connected': True,
                'currentAPVersion': '1.2.2',
                'availableAPVersion': None,
                'timeZoneId': 'CET',
                'location': {
                    'city': ' Nijmegen, Netherlands',
                    'latitude': '51.8125626',
                    'longitude': '5.8372264'
                },
                'pinAssigned': False,
                'dutyCycle': 0.5,
                'updateState': 'UP_TO_DATE',
                'powerMeterUnitPrice': 0.0,
                'powerMeterCurrency': 'EUR',
                'deviceUpdateStrategy': 'MANUALLY',
                'lastReadyForUpdateTimestamp': 1498712798641,
                'functionalHomes': {
                    'INDOOR_CLIMATE': {
                        'functionalGroups': [
                            '7c166920-e1dc-4e76-9e1b-5dac0abb02d3',
                            'f3ad2f07-1b5d-4233-8c41-04af7a878a66'],
                        'absenceType': 'NOT_ABSENT',
                        'absenceEndTime': None,
                        'floorHeatingSpecificGroups': {
                            'HEATING_TEMPERATURE_LIMITER': '84972276-92b4-41b0-9b9f-b8c10c243789',
                            'HEATING_DEHUMIDIFIER': '64a3d164-9f98-4dd7-8d4f-6f671b7c0451',
                            'HEATING_CHANGEOVER': '1f596432-372b-4267-829b-741ca7d0e802',
                            'HEATING_HUMIDITY_LIMITER': '4fec6f97-7921-44bd-a372-4d007e8eea2b',
                            'HEATING_EXTERNAL_CLOCK': 'b0c83172-1263-4591-8260-1d4f69d0f88f',
                            'HEATING_COOLING_DEMAND_BOILER': 'c92821f0-6f38-4d79-8e9c-7d74b2350787',
                            'HEATING_COOLING_DEMAND_PUMP': '82bcaa28-bf09-4131-9ae1-8b830f74c08a'
                        },
                        'ecoTemperature': 17.0,
                        'coolingEnabled': False,
                        'ecoDuration': 'PERMANENT',
                        'solution': 'INDOOR_CLIMATE',
                        'active': True
                    },
                    'LIGHT_AND_SHADOW': {
                        'functionalGroups': [
                            'cc4c1ac1-a881-41d4-b0e6-de4266b67f08'],
                        'extendedLinkedSwitchingGroups': [
                            '46ee7f5b-e3de-4182-9b95-c42fda52492e'],
                        'extendedLinkedShutterGroups': [],
                        'switchingProfileGroups': [
                            '74793b85-8245-40c4-bfe0-1e99b8009fb0'],
                        'shutterProfileGroups': [],
                        'solution': 'LIGHT_AND_SHADOW',
                        'active': True
                    },
                    'SECURITY_AND_ALARM': {
                        'functionalGroups': [
                            '21c53d30-f686-407b-847b-fa74f8980dfc'],
                        'alarmEventTimestamp': None,
                        'alarmEventDeviceId': None,
                        'alarmSecurityJournalEntryType': None,
                        'alarmActive': False,
                        'securityZones': {
                            'EXTERNAL': '64ff862e-26eb-4880-8644-fb3e9f70836e',
                            'INTERNAL': '0709ebb4-c030-4ffb-b49b-365cd0ef950d'
                        },
                        'securitySwitchingGroups': {
                            'SIREN': 'f2bc6ab0-2cfc-4538-a945-7f4887d1b8a6',
                            'PANIC': '6a4846e2-9357-45d9-9f5c-eddd29b0490b',
                            'ALARM': 'd0b1430e-bfe6-4b57-a78e-f98767d2b652',
                            'COMING_HOME': '14a8ab48-3929-4408-9a70-66eeed48d44f'
                        },
                        'zoneActivationDelay': 0.0,
                        'intrusionAlertThroughSmokeDetectors': False,
                        'solution': 'SECURITY_AND_ALARM',
                        'activationInProgress': False,
                        'active': True
                    }
                },
                'inboxGroup': '783b0268-24d6-4607-995a-ff2172dfc17b',
                'apExchangeClientId': None,
                'apExchangeState': 'NONE',
                'voiceControlSettings': {
                    'allowedActiveSecurityZoneIds': []
                },
                'ruleGroups': [],
                'id': '6b3ac3aa-be94-42d4-8af8-aa800070e0cf'
            }
        }
    },
    'origin': {
        'originType': 'DEVICE',
        'id': '3014F711A00003D3C99522FC'
    }
}
