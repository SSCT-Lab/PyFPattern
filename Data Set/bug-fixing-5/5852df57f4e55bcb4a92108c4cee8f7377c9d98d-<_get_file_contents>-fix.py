def _get_file_contents(self, file_name):
    '\n        Reads the file contents from the given file name\n\n        If the contents are vault-encrypted, it will decrypt them and return\n        the decrypted data\n\n        :arg file_name: The name of the file to read.  If this is a relative\n            path, it will be expanded relative to the basedir\n        :raises AnsibleFileNotFOund: if the file_name does not refer to a file\n        :raises AnsibleParserError: if we were unable to read the file\n        :return: Returns a byte string of the file contents\n        '
    if ((not file_name) or (not isinstance(file_name, (binary_type, text_type)))):
        raise AnsibleParserError(("Invalid filename: '%s'" % to_native(file_name)))
    b_file_name = to_bytes(self.path_dwim(file_name))
    if (not self.path_exists(b_file_name)):
        raise AnsibleFileNotFound('Unable to retrieve file contents', file_name=file_name)
    try:
        with open(b_file_name, 'rb') as f:
            data = f.read()
            return self._decrypt_if_vault_data(data, b_file_name)
    except (IOError, OSError) as e:
        raise AnsibleParserError(("an error occurred while trying to read the file '%s': %s" % (file_name, to_native(e))), orig_exc=e)