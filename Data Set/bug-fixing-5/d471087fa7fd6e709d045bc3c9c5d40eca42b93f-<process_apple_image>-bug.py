@imagetype('apple')
def process_apple_image(image):
    try:
        apple_image = {
            'uuid': six.text_type(uuid.UUID(image['uuid'])),
            'cpu_type': image.get('cpu_type'),
            'cpu_subtype': image.get('cpu_subtype'),
            'image_addr': _addr(image.get('image_addr')),
            'image_size': image['image_size'],
            'image_vmaddr': _addr((image.get('image_vmaddr') or 0)),
            'name': image.get('name'),
        }
        if (image.get('arch') is not None):
            apple_image['arch'] = image.get('arch')
        if (image.get('major_version') is not None):
            apple_image['major_version'] = image['major_version']
        if (image.get('minor_version') is not None):
            apple_image['minor_version'] = image['minor_version']
        if (image.get('revision_version') is not None):
            apple_image['revision_version'] = image['revision_version']
        return apple_image
    except KeyError as e:
        raise InterfaceValidationError(('Missing value for apple image: %s' % e.args[0]))