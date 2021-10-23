def modify_net_route(self):
    '\n        Modify a net route\n        '
    self.delete_net_route()
    route_obj = netapp_utils.zapi.NaElement('net-routes-create')
    if self.new_destination:
        route_obj.add_new_child('destination', self.new_destination)
    else:
        route_obj.add_new_child('destination', self.destination)
    if self.new_gateway:
        route_obj.add_new_child('gateway', self.new_gateway)
    else:
        route_obj.add_new_child('gateway', self.gateway)
    if self.new_metric:
        route_obj.add_new_child('metric', self.new_metric)
    else:
        route_obj.add_new_child('metric', self.metric)
    try:
        self.server.invoke_successfully(route_obj, True)
    except netapp_utils.zapi.NaApiError:
        self.create_net_route()