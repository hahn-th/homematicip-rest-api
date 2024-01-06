if __name__ == "__main__":
    import pytest
    from homematicip import __version__

    print("HMIP Version ", __version__)
    pytest.main(["-vv", "tests/aio_tests/"])
