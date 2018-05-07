if __name__ == '__main__':
    import pytest
    pytest.main('tests/test_base_connection.py')
    pytest.main('tests/test_home.py')
    pytest.main('tests/test_devices.py')
    pytest.main('tests/test_groups.py')
    pytest.main('tests/test_hmip_cli.py')
    pytest.main('tests/test_misc.py')
