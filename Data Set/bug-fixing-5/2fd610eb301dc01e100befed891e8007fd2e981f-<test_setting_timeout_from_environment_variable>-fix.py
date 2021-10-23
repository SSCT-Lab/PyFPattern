@mock.patch.dict(os.environ, {
    'DJANGO_WATCHMAN_TIMEOUT': '10',
})
def test_setting_timeout_from_environment_variable(self):
    self.assertEqual(self.RELOADER_CLS().client_timeout, 10)