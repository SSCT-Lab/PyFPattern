def remove_iso(self):
    iso = self.get_iso()
    if iso:
        self.result['changed'] = True
        args = {
            
        }
        args['id'] = iso['id']
        args['projectid'] = self.get_project('id')
        args['zoneid'] = self.get_zone('id')
        if (not self.module.check_mode):
            res = self.cs.deleteIso(**args)
    return iso