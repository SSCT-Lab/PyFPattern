

def serialize(self, obj, attrs, user):
    integration_id = None
    if obj.integration_id:
        integration_id = six.text_type(obj.integration_id)
    if obj.provider:
        provider = {
            'id': obj.provider,
            'name': obj.get_provider().name,
        }
    else:
        provider = {
            'id': 'unknown',
            'name': 'Unknown Provider',
        }
    return {
        'id': six.text_type(obj.id),
        'name': obj.name,
        'url': obj.url,
        'provider': provider,
        'status': obj.get_status_display(),
        'dateCreated': obj.date_added,
        'integrationId': integration_id,
    }
