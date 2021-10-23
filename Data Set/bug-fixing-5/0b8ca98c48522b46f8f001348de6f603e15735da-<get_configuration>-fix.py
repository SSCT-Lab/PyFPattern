def get_configuration(module, compare=False, format='xml', rollback='0'):
    if (format not in CONFIG_FORMATS):
        module.fail_json(msg='invalid config format specified')
    xattrs = {
        'format': format,
    }
    if compare:
        _validate_rollback_id(module, rollback)
        xattrs['compare'] = 'rollback'
        xattrs['rollback'] = str(rollback)
    return send_request(module, Element('get-configuration', xattrs))