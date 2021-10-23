def update_instance(self, instance, start_vm=True):
    args_service_offering = {
        
    }
    args_service_offering['id'] = instance['id']
    if self.module.params.get('service_offering'):
        args_service_offering['serviceofferingid'] = self.get_service_offering_id()
    service_offering_changed = self.has_changed(args_service_offering, instance)
    args_instance_update = {
        
    }
    args_instance_update['id'] = instance['id']
    args_instance_update['userdata'] = self.get_user_data()
    args_instance_update['ostypeid'] = self.get_os_type(key='id')
    if self.module.params.get('group'):
        args_instance_update['group'] = self.module.params.get('group')
    if self.module.params.get('display_name'):
        args_instance_update['displayname'] = self.module.params.get('display_name')
    instance_changed = self.has_changed(args_instance_update, instance)
    args_ssh_key = {
        
    }
    args_ssh_key['id'] = instance['id']
    args_ssh_key['projectid'] = self.get_project(key='id')
    if self.module.params.get('ssh_key'):
        args_ssh_key['keypair'] = self.module.params.get('ssh_key')
    ssh_key_changed = self.has_changed(args_ssh_key, instance)
    security_groups_changed = self.security_groups_has_changed()
    changed = [service_offering_changed, instance_changed, security_groups_changed, ssh_key_changed]
    if (True in changed):
        force = self.module.params.get('force')
        instance_state = instance['state'].lower()
        if ((instance_state == 'stopped') or force):
            self.result['changed'] = True
            if (not self.module.check_mode):
                instance = self.stop_instance()
                instance = self.poll_job(instance, 'virtualmachine')
                self.instance = instance
                if service_offering_changed:
                    res = self.cs.changeServiceForVirtualMachine(**args_service_offering)
                    if ('errortext' in res):
                        self.module.fail_json(msg=("Failed: '%s'" % res['errortext']))
                    instance = res['virtualmachine']
                    self.instance = instance
                if (instance_changed or security_groups_changed):
                    if security_groups_changed:
                        args_instance_update['securitygroupnames'] = ','.join(self.module.params.get('security_groups'))
                    res = self.cs.updateVirtualMachine(**args_instance_update)
                    if ('errortext' in res):
                        self.module.fail_json(msg=("Failed: '%s'" % res['errortext']))
                    instance = res['virtualmachine']
                    self.instance = instance
                if ssh_key_changed:
                    instance = self.cs.resetSSHKeyForVirtualMachine(**args_ssh_key)
                    if ('errortext' in instance):
                        self.module.fail_json(msg=("Failed: '%s'" % instance['errortext']))
                    instance = self.poll_job(instance, 'virtualmachine')
                    self.instance = instance
                if ((instance_state == 'running') and start_vm):
                    instance = self.start_instance()
    return instance