def update_on_device(self):
    params = self.changes.api_params()
    content = StringIO(self.want.content)
    self.client.api.shared.file_transfer.uploads.upload_stringio(content, self.want.filename)
    resource = self.client.api.tm.sys.file.ssl_certs.ssl_cert.load(name=self.want.filename, partition=self.want.partition)
    resource.update(**params)