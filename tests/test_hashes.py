from webhooks.hashes import placebo_hash_function, basic_hash_function


def test_placebo():
    assert placebo_hash_function() == ""


def test_basic():
    hashes = set([basic_hash_function() for x in range(30)])
    assert len(hashes) == 30
