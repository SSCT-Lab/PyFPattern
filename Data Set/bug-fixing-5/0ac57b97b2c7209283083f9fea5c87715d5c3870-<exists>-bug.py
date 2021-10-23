def exists(self):
    result = self.client.api.tm.sys.file.ssl_keys.ssl_key.exists(name=self.want.key_filename, partition=self.want.partition)
    return result