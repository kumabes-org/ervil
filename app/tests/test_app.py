"""This is the main file that we use to start tests."""


def test_sum():
    """test sum."""
    assert sum([1, 2, 3]) == 6, "Should be 6"

if __name__ == "__main__":
    test_sum()
    print("Everything passed")
