def remove_from_device(self):
    uri = 'https://{0}:{1}/mgmt/tm/gtm/server/{2}/virtual-servers/{3}'.format(self.client.provider['server'], self.client.provider['server_port'], transform_name(self.want.partition, self.want.server_name), self.want.name)
    response = self.client.api.delete(uri)
    if (response.status == 200):
        return True
    raise F5ModuleError(response.content)