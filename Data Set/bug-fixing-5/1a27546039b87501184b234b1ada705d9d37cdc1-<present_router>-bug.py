def present_router(self):
    router = self.get_router()
    if (not router):
        self.module.fail_json(msg='Router can not be created using the API, see cs_network.')
    args = {
        'id': router['id'],
        'serviceofferingid': self.get_service_offering_id(),
    }
    state = self.module.params.get('state')
    if self.has_changed(args, router):
        self.result['changed'] = True
        if (not self.module.check_mode):
            current_state = router['state'].lower()
            self.stop_router()
            router = self.cs.changeServiceForRouter(**args)
            if ('errortext' in router):
                self.module.fail_json(msg=("Failed: '%s'" % router['errortext']))
            if (state in ['restarted', 'started']):
                router = self.start_router()
            elif ((state == 'present') and (current_state == 'running')):
                router = self.start_router()
    elif (state == 'started'):
        router = self.start_router()
    elif (state == 'stopped'):
        router = self.stop_router()
    elif (state == 'restarted'):
        router = self.reboot_router()
    return router