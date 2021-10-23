@pytest.fixture
def engine(engine_and_read_ext):
    (engine, read_ext) = engine_and_read_ext
    return engine