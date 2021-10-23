def write_data(self, data, filename, shred=True):
    "Write the data bytes to given path\n\n        This is used to write a byte string to a file or stdout. It is used for\n        writing the results of vault encryption or decryption. It is used for\n        saving the ciphertext after encryption and it is also used for saving the\n        plaintext after decrypting a vault. The type of the 'data' arg should be bytes,\n        since in the plaintext case, the original contents can be of any text encoding\n        or arbitrary binary data.\n\n        When used to write the result of vault encryption, the val of the 'data' arg\n        should be a utf-8 encoded byte string and not a text typ and not a text type..\n\n        When used to write the result of vault decryption, the val of the 'data' arg\n        should be a byte string and not a text type.\n\n        :arg data: the byte string (bytes) data\n        :arg filename: filename to save 'data' to.\n        :arg shred: if shred==True, make sure that the original data is first shredded so that is cannot be recovered.\n        :returns: None\n        "
    b_file_data = to_bytes(data, errors='strict')
    output = getattr(sys.stdout, 'buffer', sys.stdout)
    if (filename == '-'):
        output.write(b_file_data)
    else:
        if os.path.isfile(filename):
            if shred:
                self._shred_file(filename)
            else:
                os.remove(filename)
        with open(filename, 'wb') as fh:
            fh.write(b_file_data)