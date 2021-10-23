def write_data(self, data, filename, shred=True):
    "write data to given path\n\n        :arg data: the encrypted and hexlified data as a utf-8 byte string\n        :arg filename: filename to save 'data' to.\n        :arg shred: if shred==True, make sure that the original data is first shredded so\n        that is cannot be recovered.\n        "
    b_file_data = to_bytes(data, errors='strict')
    if (filename == '-'):
        file_data = to_text(b_file_data, encoding='utf-8', errors='strict', nonstring='strict')
        sys.stdout.write(file_data)
    else:
        if os.path.isfile(filename):
            if shred:
                self._shred_file(filename)
            else:
                os.remove(filename)
        with open(filename, 'wb') as fh:
            fh.write(b_file_data)