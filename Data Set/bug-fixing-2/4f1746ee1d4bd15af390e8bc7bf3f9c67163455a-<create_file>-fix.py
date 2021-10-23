

def create_file(self, filename, secret, vault_id=None):
    ' create a new encrypted file '
    dirname = os.path.dirname(filename)
    if (dirname and (not os.path.exists(dirname))):
        display.warning(('%s does not exist, creating...' % dirname))
        makedirs_safe(dirname)
    if os.path.isfile(filename):
        raise AnsibleError(("%s exists, please use 'edit' instead" % filename))
    self._edit_file_helper(filename, secret, vault_id=vault_id)
