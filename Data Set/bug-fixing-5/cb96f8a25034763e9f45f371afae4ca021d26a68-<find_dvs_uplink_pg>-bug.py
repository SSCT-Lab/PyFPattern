def find_dvs_uplink_pg(self):
    if len(self.dv_switch.config.uplinkPortgroup):
        return self.dv_switch.config.uplinkPortgroup[0]
    else:
        return None