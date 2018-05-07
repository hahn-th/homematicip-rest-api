import json
from hmip_cli import getRssiBarString, anonymizeConfig


def test_getRssiBarString():
    assert getRssiBarString(-50) == '[**********]'
    assert getRssiBarString(-55) == '[*********_]'
    assert getRssiBarString(-60) == '[********__]'
    assert getRssiBarString(-65) == '[*******___]'
    assert getRssiBarString(-70) == '[******____]'
    assert getRssiBarString(-75) == '[*****_____]'
    assert getRssiBarString(-80) == '[****______]'
    assert getRssiBarString(-85) == '[***_______]'
    assert getRssiBarString(-90) == '[**________]'
    assert getRssiBarString(-95) == '[*_________]'
    assert getRssiBarString(-100) == '[__________]'

def test_anonymizeConfig():
    c = ('{"id":"d0fea2b1-ef3b-44b1-ae96-f9b31f75de84","inboxGroup":"2dc54a8d-ceee-4626-8f27-b24e78dc05de","location":'
            '{"city": "Vatican City, Vatican","latitude":"41.9026011","longitude":"12.4533701"}}')
    c = anonymizeConfig(c,'[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}','00000000-0000-0000-0000-{0:0>12}')
    #generate dummy SGTIN
    c = anonymizeConfig(c,'3014F711[A-Z0-9]{16}','3014F711{0:0>16}')
    #remove refresh Token
    c = anonymizeConfig(c,'"refreshToken": ?"[^"]+"','"refreshToken": null')
    #location
    c = anonymizeConfig(c,'"city": ?"[^"]+"','"city": "1010, Vienna, Austria"')
    c = anonymizeConfig(c,'"latitude": ?"[^"]+"','"latitude": "48.208088"')
    c = anonymizeConfig(c,'"longitude": ?"[^"]+"','"longitude": "16.358608"')

    js = json.loads(c)
    
    assert js["id"] == '00000000-0000-0000-0000-000000000000'
    assert js["inboxGroup"] == '00000000-0000-0000-0000-000000000001'
    
    l = js["location"]
    assert l["city"] == '1010, Vienna, Austria'
    assert l["latitude"] == '48.208088'
    assert l["longitude"] == '16.358608'
    

