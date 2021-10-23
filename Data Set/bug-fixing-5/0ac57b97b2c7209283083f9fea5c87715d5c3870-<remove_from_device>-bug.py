def remove_from_device(self):
    resource = self.client.api.tm.sys.file.ssl_keys.ssl_key.load(name=self.want.key_filename, partition=self.want.partition)
    resource.delete()