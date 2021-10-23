def drop_key(self, keyid):
    if (not self.module.check_mode):
        self.execute_command([self.rpm, '--erase', '--allmatches', ('gpg-pubkey-%s' % keyid[(- 8):].lower())])