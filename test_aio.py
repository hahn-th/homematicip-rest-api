if __name__ == "__main__":
    import pytest
    from homematicip import _version

    print("HMIP Version ", _version)
    pytest.main(["-vv", "tests/aio_tests/"])
