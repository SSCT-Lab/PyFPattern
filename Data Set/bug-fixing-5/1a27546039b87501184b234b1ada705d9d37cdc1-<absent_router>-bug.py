def absent_router(self):
    router = self.get_router()
    if router:
        self.result['changed'] = True
        args = {
            'id': router['id'],
        }
        if (not self.module.check_mode):
            res = self.cs.destroyRouter(**args)
            if ('errortext' in res):
                self.module.fail_json(msg=("Failed: '%s'" % res['errortext']))
            poll_async = self.module.params.get('poll_async')
            if poll_async:
                self.poll_job(res, 'router')
        return router