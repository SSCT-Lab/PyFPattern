def generate(self, module):
    'Generate the certificate signing request.'
    if ((not os.path.exists(self.path)) or self.force):
        req = crypto.X509Req()
        req.set_version(self.version)
        subject = req.get_subject()
        for (key, value) in self.subject.items():
            if (value is not None):
                setattr(subject, key, value)
        if (self.subjectAltName is not None):
            req.add_extensions([crypto.X509Extension(b'subjectAltName', False, self.subjectAltName.encode('ascii'))])
        privatekey_content = open(self.privatekey_path).read()
        self.privatekey = crypto.load_privatekey(crypto.FILETYPE_PEM, privatekey_content)
        req.set_pubkey(self.privatekey)
        req.sign(self.privatekey, self.digest)
        self.request = req
        try:
            csr_file = open(self.path, 'wb')
            csr_file.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, self.request))
            csr_file.close()
        except (IOError, OSError) as exc:
            raise CertificateSigningRequestError(exc)
    else:
        self.changed = False
    file_args = module.load_file_common_arguments(module.params)
    if module.set_fs_attributes_if_different(file_args, False):
        self.changed = True