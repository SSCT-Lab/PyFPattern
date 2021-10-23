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
            if ('errortext' in res):
                self.module.fail_json(msg=("Failed: '%s'" % res['errortext']))
            poll_async = self.module.params.get('poll_async')
            if poll_async:
                self.poll_job(res, 'iso')
    return iso