if __name__ == '__main__':
    import pytest
    from homematicip import __version__
    print("HMIP Version ", __version__)
    pytest.main('tests/test_devices.py -vv')
