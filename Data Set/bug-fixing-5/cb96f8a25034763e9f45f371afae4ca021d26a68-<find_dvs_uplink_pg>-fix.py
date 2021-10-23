def find_dvs_uplink_pg(self):
    dvs_uplink_pg = (self.dv_switch.config.uplinkPortgroup[0] if len(self.dv_switch.config.uplinkPortgroup) else None)
    return dvs_uplink_pg