def create_sample_event(project, platform=None, default=None, raw=True, sample_name=None, **kwargs):
    if ((not platform) and (not default)):
        return
    timestamp = kwargs.get('timestamp')
    data = load_data(platform, default, timestamp, sample_name)
    if (not data):
        return
    data.update(kwargs)
    data = ClientApiHelper().validate_data(data)
    manager = EventManager(data)
    manager.normalize()
    return manager.save(project.id, raw=raw)