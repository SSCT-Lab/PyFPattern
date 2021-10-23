def _construct_url_1(self, obj, child_includes):
    '\n        This method is used by get_url when the object is the top-level class.\n        '
    obj_class = obj['aci_class']
    obj_rn = obj['aci_rn']
    mo = obj['module_object']
    if (self.module.params['state'] != 'query'):
        path = 'api/mo/uni/{}.json'.format(obj_rn)
        filter_string = ('?rsp-prop-include=config-only' + child_includes)
    elif (mo is None):
        path = 'api/class/{}.json'.format(obj_class)
        filter_string = ''
    else:
        path = 'api/mo/uni/{}.json'.format(obj_rn)
        filter_string = ''
    if ((child_includes is not None) and (filter_string == '')):
        filter_string = child_includes.replace('&', '?', 1)
    return (path, filter_string)