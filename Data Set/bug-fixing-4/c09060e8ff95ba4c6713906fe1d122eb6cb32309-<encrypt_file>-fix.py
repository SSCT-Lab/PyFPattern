def encrypt_file(self, filename, output_file=None):
    check_prereqs()
    b_plaintext = self.read_data(filename)
    b_ciphertext = self.vault.encrypt(b_plaintext)
    self.write_data(b_ciphertext, (output_file or filename))