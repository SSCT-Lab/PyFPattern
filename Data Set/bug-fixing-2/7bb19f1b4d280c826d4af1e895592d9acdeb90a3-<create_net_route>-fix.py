

def create_net_route(self, current_metric=None):
    '\n        Creates a new Route\n        '
    route_obj = netapp_utils.zapi.NaElement('net-routes-create')
    route_obj.add_new_child('destination', self.parameters['destination'])
    route_obj.add_new_child('gateway', self.parameters['gateway'])
    if ((current_metric is None) and (self.parameters.get('metric') is not None)):
        metric = self.parameters['metric']
    else:
        metric = current_metric
    if (metric is not None):
        route_obj.add_new_child('metric', metric)
    try:
        self.server.invoke_successfully(route_obj, True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error creating net route: %s' % to_native(error)), exception=traceback.format_exc())
