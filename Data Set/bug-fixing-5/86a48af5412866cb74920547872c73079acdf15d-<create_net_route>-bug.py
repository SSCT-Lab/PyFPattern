def create_net_route(self):
    '\n        Creates a new Route\n        '
    route_obj = netapp_utils.zapi.NaElement('net-routes-create')
    route_obj.add_new_child('destination', self.destination)
    route_obj.add_new_child('gateway', self.gateway)
    if self.metric:
        route_obj.add_new_child('metric', self.metric)
    try:
        self.server.invoke_successfully(route_obj, True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error creating net route: %s' % to_native(error)), exception=traceback.format_exc())