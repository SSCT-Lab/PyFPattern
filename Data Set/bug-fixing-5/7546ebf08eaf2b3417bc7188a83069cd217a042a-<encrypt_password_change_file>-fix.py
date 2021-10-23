def encrypt_password_change_file(self, public_key, password):
    pub = serialization.load_pem_public_key(to_bytes(public_key), backend=default_backend())
    message = to_bytes('{0}\n{0}\n'.format(password))
    ciphertext = pub.encrypt(message, padding.PKCS1v15())
    return BytesIO(ciphertext)