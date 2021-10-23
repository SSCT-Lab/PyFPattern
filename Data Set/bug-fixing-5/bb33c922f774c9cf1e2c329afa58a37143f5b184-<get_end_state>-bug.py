def get_end_state(self):
    'get end state information'
    self.get_static_route(self.state)
    self.end_state['sroute'] = self.static_routes_info['sroute']