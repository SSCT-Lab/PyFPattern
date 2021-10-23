def apply(self):
    '\n        Run Module based on play book\n        '
    changed = False
    netapp_utils.ems_log_event('na_ontap_net_routes', self.server)
    route_exists = False
    existing_route = self.does_route_exists()
    if existing_route:
        route_exists = True
        if (self.state == 'absent'):
            changed = True
        elif (self.state == 'present'):
            if (self.new_destination or self.new_gateway or self.new_metric):
                changed = True
    elif (self.state == 'present'):
        changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (not route_exists):
            if (self.state == 'present'):
                self.create_net_route()
        elif (self.state == 'present'):
            self.modify_net_route()
        elif (self.state == 'absent'):
            self.delete_net_route()
    self.module.exit_json(changed=changed)