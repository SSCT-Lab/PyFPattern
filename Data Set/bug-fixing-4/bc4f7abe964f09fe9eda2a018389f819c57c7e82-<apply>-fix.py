def apply(self):
    ' calling all adapter features '
    changed = False
    results = netapp_utils.get_cserver(self.server)
    cserver = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=results)
    netapp_utils.ems_log_event('na_ontap_ucadapter', cserver)
    adapter_detail = self.get_adapter()

    def need_to_change(expected, pending, current):
        if (expected is None):
            return False
        if (pending is not None):
            return (pending != expected)
        if (current is not None):
            return (current != expected)
        return False
    if adapter_detail:
        changed = (need_to_change(self.type, adapter_detail['pending-type'], adapter_detail['type']) or need_to_change(self.mode, adapter_detail['pending-mode'], adapter_detail['mode']))
    if changed:
        if self.module.check_mode:
            pass
        else:
            self.offline_adapter()
            self.modify_adapter()
            self.online_adapter()
    self.module.exit_json(changed=changed)