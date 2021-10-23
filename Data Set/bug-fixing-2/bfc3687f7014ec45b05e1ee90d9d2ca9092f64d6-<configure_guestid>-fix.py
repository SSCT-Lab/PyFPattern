

def configure_guestid(self, vm_obj, vm_creation=False):
    if self.params['template']:
        return
    if (vm_creation and (self.params['guest_id'] is None)):
        self.module.fail_json(msg='guest_id attribute is mandatory for VM creation')
    if (self.params['guest_id'] and ((vm_obj is None) or (self.params['guest_id'].lower() != vm_obj.summary.config.guestId.lower()))):
        self.change_detected = True
        self.configspec.guestId = self.params['guest_id']
