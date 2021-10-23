def remove_virtual_disk_from_device(self):
    response = self.get_virtual_disk_on_device()
    uri = 'https://{0}:{1}/mgmt/tm/vcmp/virtual-disk/{2}'.format(self.client.provider['server'], self.client.provider['server_port'], response['name'])
    response = self.client.api.delete(uri)
    if (response.status == 200):
        return True
    raise F5ModuleError(response.content)