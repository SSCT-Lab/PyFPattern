def configure_guestid(self, vm_obj, vm_creation=False):
    if (self.should_deploy_from_template() and (self.params.get('guest_id') is None)):
        return
    if (vm_creation and (self.params['guest_id'] is None)):
        self.module.fail_json(msg='guest_id attribute is mandatory for VM creation')
    if ((vm_obj is None) or (self.params['guest_id'] != vm_obj.summary.config.guestId)):
        self.change_detected = True
        self.configspec.guestId = self.params['guest_id']