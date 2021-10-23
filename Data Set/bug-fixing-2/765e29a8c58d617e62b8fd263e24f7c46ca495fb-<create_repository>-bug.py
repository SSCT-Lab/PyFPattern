

def create_repository(self, organization, data):
    integration = Integration.objects.get(id=data['integration_id'], provider=self.repo_provider)
    base_url = integration.metadata.get('domain_name')
    return {
        'name': data['identifier'],
        'external_id': data['external_id'],
        'url': 'https://{}/{}'.format(base_url, data['identifier']),
        'config': {
            'name': data['identifier'],
        },
        'integration_id': data['integration_id'],
    }
