def cg_start(self):
    '\n        For the given list of volumes, creates cg-snapshot\n        '
    snapshot_started = False
    cgstart = netapp_utils.zapi.NaElement('cg-start')
    cgstart.add_new_child('snapshot', self.snapshot)
    cgstart.add_new_child('timeout', self.timeout)
    volume_list = netapp_utils.zapi.NaElement('volumes')
    cgstart.add_child_elem(volume_list)
    for vol in self.volumes:
        snapshot_exists = self.does_snapshot_exist(vol)
        if (snapshot_exists is None):
            snapshot_started = True
            volume_list.add_new_child('volume-name', vol)
    if snapshot_started:
        if self.snapmirror_label:
            cgstart.add_new_child('snapmirror-label', self.snapmirror_label)
        try:
            cgresult = self.server.invoke_successfully(cgstart, enable_tunneling=True)
            if cgresult.has_attr('cg-id'):
                self.cgid = cgresult['cg-id']
        except netapp_utils.zapi.NaApiError as error:
            self.module.fail_json(msg=('Error creating CG snapshot %s: %s' % (self.snapshot, to_native(error))), exception=traceback.format_exc())
    return snapshot_started