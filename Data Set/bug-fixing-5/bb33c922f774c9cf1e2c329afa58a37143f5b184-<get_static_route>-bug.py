def get_static_route(self, state):
    'get ipv4 static route'
    self.static_routes_info['sroute'] = list()
    if (state == 'absent'):
        getxmlstr = CE_NC_GET_STATIC_ROUTE_ABSENT
    else:
        getxmlstr = CE_NC_GET_STATIC_ROUTE
    xml_str = get_nc_config(self.module, getxmlstr)
    if ('data/' in xml_str):
        return
    xml_str = xml_str.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
    root = ElementTree.fromstring(xml_str)
    static_routes = root.findall('data/staticrt/staticrtbase/srRoutes/srRoute')
    if static_routes:
        for static_route in static_routes:
            static_info = dict()
            for static_ele in static_route:
                if (static_ele.tag in ['vrfName', 'afType', 'topologyName', 'prefix', 'maskLength', 'destVrfName', 'nexthop', 'ifName', 'preference', 'description']):
                    static_info[static_ele.tag] = static_ele.text
                if (static_ele.tag == 'tag'):
                    if (static_ele.text is not None):
                        static_info['tag'] = static_ele.text
                    else:
                        static_info['tag'] = 'None'
            self.static_routes_info['sroute'].append(static_info)