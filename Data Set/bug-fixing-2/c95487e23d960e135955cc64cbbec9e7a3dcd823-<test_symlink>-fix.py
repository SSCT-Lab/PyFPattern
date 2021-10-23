

def test_symlink(self):
    if hasattr(os, 'symlink'):
        if os.path.exists(self.symlinked_dir):
            self.assertTrue(os.path.islink(self.symlinked_dir))
        else:
            try:
                os.symlink(os.path.join(self.test_dir, 'templates'), self.symlinked_dir)
            except (OSError, NotImplementedError):
                raise SkipTest("os.symlink() is available on this OS but can't be used by this user.")
        os.chdir(self.test_dir)
        management.call_command('makemessages', locale=[LOCALE], verbosity=0, symlinks=True)
        self.assertTrue(os.path.exists(self.PO_FILE))
        with open(self.PO_FILE, 'r') as fp:
            po_contents = force_text(fp.read())
            self.assertMsgId('This literal should be included.', po_contents)
            self.assertIn(os.path.join('templates_symlinked', 'test.html'), po_contents)
