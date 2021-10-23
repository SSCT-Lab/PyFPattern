def load_configuration(module, candidate=None, action='merge', rollback=None, format='xml'):
    if all(((candidate is None), (rollback is None))):
        module.fail_json(msg='one of candidate or rollback must be specified')
    elif all(((candidate is not None), (rollback is not None))):
        module.fail_json(msg='candidate and rollback are mutually exclusive')
    if (format not in FORMATS):
        module.fail_json(msg='invalid format specified')
    if ((format == 'json') and (action not in JSON_ACTIONS)):
        module.fail_json(msg='invalid action for format json')
    elif ((format in ('text', 'xml')) and (action not in ACTIONS)):
        module.fail_json(msg=('invalid action format %s' % format))
    if ((action == 'set') and (not (format == 'text'))):
        module.fail_json(msg='format must be text when action is set')
    if (rollback is not None):
        _validate_rollback_id(module, rollback)
        xattrs = {
            'rollback': str(rollback),
        }
    else:
        xattrs = {
            'action': action,
            'format': format,
        }
    obj = Element('load-configuration', xattrs)
    if (candidate is not None):
        lookup = {
            'xml': 'configuration',
            'text': 'configuration-text',
            'set': 'configuration-set',
            'json': 'configuration-json',
        }
        if (action == 'set'):
            cfg = SubElement(obj, 'configuration-set')
        else:
            cfg = SubElement(obj, lookup[format])
        if isinstance(candidate, string_types):
            cfg.text = candidate
        else:
            cfg.append(candidate)
    return send_request(module, obj)