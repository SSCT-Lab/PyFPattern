@imagetype('proguard')
def process_proguard_image(image):
    try:
        if (image['uuid'] is None):
            raise KeyError('uuid')
        return {
            'uuid': six.text_type(uuid.UUID(image['uuid'])),
        }
    except KeyError as e:
        raise InterfaceValidationError(('Missing value for proguard image: %s' % e.args[0]))