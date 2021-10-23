def test_msgfmt_error_including_non_ascii(self):
    mo_file = 'locale/ko/LC_MESSAGES/django.mo'
    self.addCleanup(self.rmfile, os.path.join(self.test_dir, mo_file))
    env = os.environ.copy()
    env.update({
        str('LANG'): str('C'),
    })
    with mock.patch('django.core.management.utils.Popen', (lambda *args, **kwargs: Popen(*args, env=env, **kwargs))):
        if six.PY2:
            try:
                call_command('compilemessages', locale=['ko'], verbosity=0)
            except CommandError as err:
                self.assertIn("' cannot start a field name", six.text_type(err))
        else:
            cmd = MakeMessagesCommand()
            if (cmd.gettext_version < (0, 18, 3)):
                raise unittest.SkipTest('python-brace-format is a recent gettext addition.')
            with self.assertRaisesMessage(CommandError, "' cannot start a field name"):
                call_command('compilemessages', locale=['ko'], verbosity=0)