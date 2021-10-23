def delete_net_route(self):
    '\n        Deletes a given Route\n        '
    route_obj = netapp_utils.zapi.NaElement('net-routes-destroy')
    route_obj.add_new_child('destination', self.destination)
    route_obj.add_new_child('gateway', self.gateway)
    try:
        self.server.invoke_successfully(route_obj, True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error deleting net route: %s' % to_native(error)), exception=traceback.format_exc())