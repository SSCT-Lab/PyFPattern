

def remove_from_device(self):
    uri = 'https://{0}:{1}/mgmt/shared/appsvcs/declare/{2}'.format(self.client.provider['server'], self.client.provider['server_port'], self.want.tenants)
    response = self.client.api.delete(uri)
    if (response.status != 200):
        result = response.json()
        errors = self._get_errors_from_response(result)
        if errors:
            message = '{0}'.format('. '.join(errors))
            raise F5ModuleError(message)
        raise F5ModuleError(response.content)
