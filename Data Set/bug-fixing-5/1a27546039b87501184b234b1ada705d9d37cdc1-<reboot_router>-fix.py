def reboot_router(self):
    router = self.get_router()
    if (not router):
        self.module.fail_json(msg='Router not found')
    self.result['changed'] = True
    args = {
        'id': router['id'],
    }
    if (not self.module.check_mode):
        res = self.query_api('rebootRouter', **args)
        poll_async = self.module.params.get('poll_async')
        if poll_async:
            router = self.poll_job(res, 'router')
    return router