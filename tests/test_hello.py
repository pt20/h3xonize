import pytest


@pytest.mark.parametrize("inp,expected", [(2, 4), (-2, 0)], ids=["positive", "negative"])
def test_add_two(inp, expected):
    assert 2 + inp == expected
