def test_django_admin_py_deprecated(self):
    (_, err) = self._run_test(['-Wd', self.django_admin_py, '--version'])
    self.assertIn(self.DEPRECATION_MESSAGE, err)