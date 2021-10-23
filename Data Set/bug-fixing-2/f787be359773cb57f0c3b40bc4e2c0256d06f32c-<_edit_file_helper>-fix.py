

def _edit_file_helper(self, filename, secret, existing_data=None, force_save=False, vault_id=None):
    (root, ext) = os.path.splitext(os.path.realpath(filename))
    (fd, tmp_path) = tempfile.mkstemp(suffix=ext)
    os.close(fd)
    try:
        if existing_data:
            self.write_data(existing_data, tmp_path, shred=False)
        subprocess.call(self._editor_shell_command(tmp_path))
    except:
        self._shred_file(tmp_path)
        raise
    b_tmpdata = self.read_data(tmp_path)
    if ((existing_data == b_tmpdata) and (not force_save)):
        self._shred_file(tmp_path)
        return
    b_ciphertext = self.vault.encrypt(b_tmpdata, secret, vault_id=vault_id)
    self.write_data(b_ciphertext, tmp_path)
    self.shuffle_files(tmp_path, filename)
