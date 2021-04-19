from vizcovidfr.maps import maps


def test_viz2Dmap():
    """
    Test viz2Dmap by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will be raised
    """
    result = (type(maps.viz2Dmap()) != int)
    assert result


def test_viz3Dmap():
    """
    Test viz3Dmap by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will be raised
    """
    result = (type(maps.viz3Dmap()) != int)
    assert result


def test_transfer_map():
    """
    Test transfer_map by running the function.
    If something fails while running it, result won't be defined,
    and an AssertionError will be raised
    """
    result = (type(maps.transfer_map()) != int)
    assert result
