def _construct_url_2(self, parent, obj, child_includes):
    '\n        This method is used by get_url when the object is the second-level class.\n        '
    parent_rn = parent['aci_rn']
    parent_obj = parent['module_object']
    obj_class = obj['aci_class']
    obj_rn = obj['aci_rn']
    obj_filter = obj['filter_target']
    obj = obj['module_object']
    if (not child_includes):
        self_child_includes = ('?rsp-subtree=full&rsp-subtree-class=' + obj_class)
    else:
        self_child_includes = ((child_includes.replace('&', '?', 1) + ',') + obj_class)
    if (self.module.params['state'] != 'query'):
        path = 'api/mo/uni/{}/{}.json'.format(parent_rn, obj_rn)
        filter_string = ('?rsp-prop-include=config-only' + child_includes)
    elif ((obj is None) and (parent_obj is None)):
        path = 'api/class/{}.json'.format(obj_class)
        filter_string = ''
    elif (parent_obj is not None):
        if (obj is not None):
            path = 'api/mo/uni/{}/{}.json'.format(parent_rn, obj_rn)
            filter_string = ''
        else:
            path = 'api/mo/uni/{}.json'.format(parent_rn)
            filter_string = self_child_includes
    else:
        path = 'api/class/{}.json'.format(obj_class)
        filter_string = ('?query-target-filter=eq{}'.format(obj_filter) + child_includes)
    if ((child_includes is not None) and (filter_string == '')):
        filter_string = child_includes.replace('&', '?', 1)
    return (path, filter_string)