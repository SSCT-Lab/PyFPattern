

def remove_from_device(self):
    uri = 'https://{0}:{1}/mgmt/shared/appsvcs/declare/{2}'.format(self.client.provider['server'], self.client.provider['server_port'], self.want.tenants)
    response = self.client.api.delete(uri)
    if (response.status == 200):
        return True
    raise F5ModuleError(response.content)
