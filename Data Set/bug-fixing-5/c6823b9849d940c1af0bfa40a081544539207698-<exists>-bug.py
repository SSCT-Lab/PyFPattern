def exists(self):
    result = self.client.api.tm.sys.file.ssl_certs.ssl_cert.exists(name=self.want.filename, partition=self.want.partition)
    return result