def remove_from_device(self):
    resource = self.client.api.tm.sys.file.ssl_certs.ssl_cert.load(name=self.want.filename, partition=self.want.partition)
    resource.delete()