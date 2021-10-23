@pytest.fixture(autouse=True)
def XenAPI():
    'Imports and returns fake XenAPI module.'
    fake_xenapi = importlib.import_module('units.module_utils.xenserver.FakeXenAPI')
    sys.modules['XenAPI'] = fake_xenapi
    return fake_xenapi