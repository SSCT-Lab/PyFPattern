def set_queue_attribute(queue, attribute, value, check_mode=False):
    if ((not value) and (value != 0)):
        return False
    try:
        existing_value = queue.get_attributes(attributes=attribute)[attribute]
    except:
        existing_value = ''
    if (attribute in ['Policy', 'RedrivePolicy']):
        value = json.dumps(value, sort_keys=True)
        if existing_value:
            existing_value = json.dumps(json.loads(existing_value), sort_keys=True)
    if (str(value) != existing_value):
        if (not check_mode):
            queue.set_attribute(attribute, value)
        return True
    return False