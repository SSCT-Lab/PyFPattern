def pytest_runtest_setup(item):
    if (('slow' in item.keywords) and item.config.getoption('--skip-slow')):
        pytest.skip('skipping due to --skip-slow')
    if (('slow' not in item.keywords) and item.config.getoption('--only-slow')):
        pytest.skip('skipping due to --only-slow')
    if (('network' in item.keywords) and item.config.getoption('--skip-network')):
        pytest.skip('skipping due to --skip-network')
    if (('high_memory' in item.keywords) and (not item.config.getoption('--run-high-memory'))):
        pytest.skip('skipping high memory test since --run-high-memory was not set')
    pattern = item.config.getoption('-m')
    if (('db' in item.keywords) and (not pattern)):
        pytest.skip('skipping db unless -m "db" is specified')
    elif (('db' in item.keywords) and pattern):
        markers = collections.defaultdict(bool)
        for marker in item.iter_markers():
            markers[marker.name] = True
        markers['db'] = False
        db_in_pattern = (not eval(pattern, {
            
        }, markers))
        if (not db_in_pattern):
            pytest.skip('skipping db unless -m "db" is specified')