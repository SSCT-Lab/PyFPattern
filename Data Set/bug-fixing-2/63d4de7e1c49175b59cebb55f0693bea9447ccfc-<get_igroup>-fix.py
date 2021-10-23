

def get_igroup(self, name):
    '\n        Return details about the igroup\n        :param:\n            name : Name of the igroup\n\n        :return: Details about the igroup. None if not found.\n        :rtype: dict\n        '
    igroup_info = netapp_utils.zapi.NaElement('igroup-get-iter')
    attributes = dict(query={
        'initiator-group-info': {
            'initiator-group-name': name,
            'vserver': self.parameters['vserver'],
        },
    })
    igroup_info.translate_struct(attributes)
    (result, current) = (None, None)
    try:
        result = self.server.invoke_successfully(igroup_info, True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error fetching igroup info %s: %s' % (self.parameters['name'], to_native(error))), exception=traceback.format_exc())
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        igroup = result.get_child_by_name('attributes-list').get_child_by_name('initiator-group-info')
        initiators = []
        if igroup.get_child_by_name('initiators'):
            current_initiators = igroup['initiators'].get_children()
            for initiator in current_initiators:
                initiators.append(initiator['initiator-name'])
        current = {
            'initiators': initiators,
        }
    return current
