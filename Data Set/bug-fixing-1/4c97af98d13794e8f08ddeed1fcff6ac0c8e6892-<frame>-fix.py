

@pytest.fixture
def frame(float_frame):
    '\n    Returns the first ten items in fixture "float_frame".\n    '
    return float_frame[:10]
