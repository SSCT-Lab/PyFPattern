def test_django_admin_py_equivalent_main(self):
    django_admin_py = ((Path(django.__file__).parent / 'bin') / 'django-admin.py')
    (django_admin_py_out, _) = self._run_test([django_admin_py, '--version'])
    (django_out, _) = self._run_test(['-m', 'django', '--version'])
    self.assertEqual(django_admin_py_out, django_out)