

def setUp(self):
    self._cwd = os.getcwd()
    self.work_dir = tempfile.mkdtemp(prefix='i18n_')
    self.test_dir = os.path.abspath(os.path.join(self.work_dir, self.work_subdir))
    copytree(os.path.join(source_code_dir, self.work_subdir), self.test_dir)
    self.addCleanup(self._rmrf, self.test_dir)
    self.addCleanup(os.chdir, self._cwd)
    os.chdir(self.test_dir)
