def serialize(self, obj, attrs, user, *args, **kwargs):
    return {
        'id': six.text_type(obj.id),
        'environment': attrs.get('environment'),
        'dateStarted': obj.date_started,
        'dateFinished': obj.date_finished,
        'name': obj.name,
        'url': obj.url,
    }