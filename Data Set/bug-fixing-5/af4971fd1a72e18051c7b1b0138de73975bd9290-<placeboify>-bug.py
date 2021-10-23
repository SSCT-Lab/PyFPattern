@pytest.fixture
def placeboify(request, monkeypatch):
    "This fixture puts a recording/replaying harness around `boto3_conn`\n\n    Placeboify patches the `boto3_conn` function in ec2 module_utils to return\n    a boto3 session that in recording or replaying mode, depending on the\n    PLACEBO_RECORD environment variable. Unset PLACEBO_RECORD (the common case\n    for just running tests) will put placebo in replay mode, set PLACEBO_RECORD\n    to any value to turn off replay & operate on real AWS resources.\n\n    The recorded sessions are stored in the test file's directory, under the\n    namespace `placebo_recordings/{testfile name}/{test function name}` to\n    distinguish them.\n    "
    session = boto3.Session(region_name='us-west-2')
    recordings_path = os.path.join(request.fspath.dirname, 'placebo_recordings', request.fspath.basename.replace('.py', ''), request.function.__name__).replace('test_', '')
    try:
        os.makedirs(recordings_path)
    except OSError as e:
        if (e.errno != errno.EEXIST):
            raise
    pill = placebo.attach(session, data_path=recordings_path)
    if os.getenv('PLACEBO_RECORD'):
        pill.record()
    else:
        pill.playback()

    def boto3_middleman_connection(module, conn_type, resource, region='us-west-2', **kwargs):
        if (conn_type != 'client'):
            raise ValueError(('Mocker only supports client, not %s' % conn_type))
        return session.client(resource, region_name=region)
    import ansible.module_utils.ec2
    monkeypatch.setattr(ansible.module_utils.ec2, 'boto3_conn', boto3_middleman_connection)
    (yield session)
    pill.stop()