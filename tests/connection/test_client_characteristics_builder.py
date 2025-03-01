from homematicip.connection.client_characteristics_builder import (ClientCharacteristicsBuilder)


def test_client_characteristics_builder():
    access_point_id = "3014F711A000000000000355"
    cc = ClientCharacteristicsBuilder.get(access_point_id)
    assert cc['id'] == access_point_id
