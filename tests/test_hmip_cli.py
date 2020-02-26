import json

from hmip_cli import getRssiBarString
from homematicip.base.helpers import anonymizeConfig, handle_config


def test_getRssiBarString():
    assert getRssiBarString(-50) == "[**********]"
    assert getRssiBarString(-55) == "[*********_]"
    assert getRssiBarString(-60) == "[********__]"
    assert getRssiBarString(-65) == "[*******___]"
    assert getRssiBarString(-70) == "[******____]"
    assert getRssiBarString(-75) == "[*****_____]"
    assert getRssiBarString(-80) == "[****______]"
    assert getRssiBarString(-85) == "[***_______]"
    assert getRssiBarString(-90) == "[**________]"
    assert getRssiBarString(-95) == "[*_________]"
    assert getRssiBarString(-100) == "[__________]"


def test_handle_config_error():
    assert handle_config({"errorCode": "Dummy"}, False) is None


def test_anonymizeConfig():
    c = (
        '{"id":"d0fea2b1-ef3b-44b1-ae96-f9b31f75de84",'
        '"id2":"d0fea2b1-ef3b-44b1-ae96-f9b31f75de84",'
        '"inboxGroup":"2dc54a8d-ceee-4626-8f27-b24e78dc05de",'
        '"availableFirmwareVersion": "0.0.0",'
        '"sgtin":"3014F71112345AB891234561", "sgtin_silvercrest" : "301503771234567891234567",'
        '"location":'
        '{"city": "Vatican City, Vatican","latitude":"41.9026011","longitude":"12.4533701"}}'
    )
    c = handle_config(json.loads(c), True)

    js = json.loads(c)

    assert js["id"] == "00000000-0000-0000-0000-000000000000"
    assert js["id"] == js["id2"]
    assert js["inboxGroup"] == "00000000-0000-0000-0000-000000000001"
    assert js["sgtin"] == "3014F7110000000000000000"
    assert js["sgtin_silvercrest"] == "3014F7110000000000000001"
    assert js["availableFirmwareVersion"] == "0.0.0"

    l = js["location"]
    assert l["city"] == "1010, Vienna, Austria"
    assert l["latitude"] == "48.208088"
    assert l["longitude"] == "16.358608"

    c = '{"id":"test"}'
    c = anonymizeConfig(c, "original", "REPLACED")
    assert c == '{"id":"test"}'
