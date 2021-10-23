def update_on_device(self):
    content = StringIO(self.want.content)
    self.client.api.shared.file_transfer.uploads.upload_stringio(content, self.want.key_filename)
    resource = self.client.api.tm.sys.file.ssl_keys.ssl_key.load(name=self.want.key_filename, partition=self.want.partition)
    resource.update()