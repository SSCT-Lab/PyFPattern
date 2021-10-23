def create_on_device(self):
    content = StringIO(self.want.content)
    self.client.api.shared.file_transfer.uploads.upload_stringio(content, self.want.filename)
    resource = self.client.api.tm.sys.file.ssl_certs.ssl_cert.create(sourcePath=self.want.source_path, name=self.want.filename, partition=self.want.partition)
    params = self.want.api_params()
    if params:
        resource.update(**params)