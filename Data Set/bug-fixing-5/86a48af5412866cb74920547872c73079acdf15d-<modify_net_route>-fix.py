def modify_net_route(self, current, desired):
    '\n        Modify a net route\n        '
    for (key, val) in desired.items():
        if (val == current[key]):
            self.na_helper.changed = False
            return
    self.delete_net_route()
    route_obj = netapp_utils.zapi.NaElement('net-routes-create')
    for attribute in ['metric', 'destination', 'gateway']:
        if (desired.get(attribute) is not None):
            value = desired[attribute]
        else:
            value = current[attribute]
        route_obj.add_new_child(attribute, value)
    try:
        result = self.server.invoke_successfully(route_obj, True)
    except netapp_utils.zapi.NaApiError as error:
        self.create_net_route(current['metric'])
        if (to_native(error.code) == '13001'):
            return
        self.module.fail_json(msg=('Error modifying net route: %s' % to_native(error)), exception=traceback.format_exc())