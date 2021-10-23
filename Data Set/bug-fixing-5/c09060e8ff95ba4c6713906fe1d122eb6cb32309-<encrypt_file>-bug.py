def encrypt_file(self, filename, output_file=None):
    check_prereqs()
    plaintext = self.read_data(filename)
    ciphertext = self.vault.encrypt(plaintext)
    self.write_data(ciphertext, (output_file or filename))