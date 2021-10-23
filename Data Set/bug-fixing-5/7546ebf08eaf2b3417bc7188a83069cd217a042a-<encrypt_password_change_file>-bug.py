def encrypt_password_change_file(self, public_key, password):
    pub = serialization.load_pem_public_key(bytes(public_key, 'utf-8'), backend=default_backend())
    message = bytes('{0}\n{0}\n'.format(password), 'utf-8')
    ciphertext = pub.encrypt(message, padding.PKCS1v15())
    return BytesIO(ciphertext)