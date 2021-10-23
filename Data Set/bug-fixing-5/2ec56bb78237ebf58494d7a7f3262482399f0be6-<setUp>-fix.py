def setUp(self):
    self.temp_dir = tempfile.TemporaryDirectory()
    self.addCleanup(self.temp_dir.cleanup)
    template_settings_py = os.path.join(os.path.dirname(conf.__file__), 'project_template', 'project_name', 'settings.py-tpl')
    test_settings_py = os.path.join(self.temp_dir.name, 'test_settings.py')
    shutil.copyfile(template_settings_py, test_settings_py)