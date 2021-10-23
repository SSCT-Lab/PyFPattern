def ensure_integration(key, data):
    defaults = {
        'metadata': data.get('metadata', {
            
        }),
        'name': data.get('name', data['external_id']),
        'status': ObjectStatus.VISIBLE,
    }
    (integration, created) = Integration.objects.get_or_create(provider=key, external_id=data['external_id'], defaults=defaults)
    if (not created):
        integration.update(**defaults)
    return integration