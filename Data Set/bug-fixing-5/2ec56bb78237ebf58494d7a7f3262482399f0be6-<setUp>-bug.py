def setUp(self):
    project_dir = os.path.join(os.path.dirname(conf.__file__), 'project_template', 'project_name')
    template_settings_py = os.path.join(project_dir, 'settings.py-tpl')
    test_settings_py = os.path.join(project_dir, 'settings.py')
    shutil.copyfile(template_settings_py, test_settings_py)
    self.addCleanup(os.remove, test_settings_py)