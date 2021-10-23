def test_django_admin_py_deprecated(self):
    django_admin_py = ((Path(django.__file__).parent / 'bin') / 'django-admin.py')
    (_, err) = self._run_test(['-Wd', django_admin_py, '--version'])
    self.assertIn(self.DEPRECATION_MESSAGE, err)