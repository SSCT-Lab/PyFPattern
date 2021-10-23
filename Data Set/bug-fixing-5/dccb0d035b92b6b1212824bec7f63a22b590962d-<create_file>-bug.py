def create_file(self, filename, secret, vault_id=None):
    ' create a new encrypted file '
    if os.path.isfile(filename):
        raise AnsibleError(("%s exists, please use 'edit' instead" % filename))
    self._edit_file_helper(filename, secret, vault_id=vault_id)