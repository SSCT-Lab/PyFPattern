

def run(self):
    self.test_parameter_versions()
    module = self.client.module
    try:
        current_service = self.get_service(module.params['name'])
    except Exception as e:
        return module.fail_json(msg=('Error looking for service named %s: %s' % (module.params['name'], e)))
    try:
        new_service = DockerService.from_ansible_params(module.params, current_service)
    except Exception as e:
        return module.fail_json(msg=('Error parsing module parameters: %s' % e))
    changed = False
    msg = 'noop'
    rebuilt = False
    changes = []
    facts = {
        
    }
    if current_service:
        if (module.params['state'] == 'absent'):
            if (not module.check_mode):
                self.remove_service(module.params['name'])
            msg = 'Service removed'
            changed = True
        else:
            (changed, changes, need_rebuild, force_update) = new_service.compare(current_service)
            if changed:
                if need_rebuild:
                    if (not module.check_mode):
                        self.remove_service(module.params['name'])
                        self.create_service(module.params['name'], new_service)
                    msg = 'Service rebuilt'
                    rebuilt = True
                else:
                    if (not module.check_mode):
                        self.update_service(module.params['name'], current_service, new_service)
                    msg = 'Service updated'
                    rebuilt = False
            elif force_update:
                if (not module.check_mode):
                    self.update_service(module.params['name'], current_service, new_service)
                msg = 'Service forcefully updated'
                rebuilt = False
                changed = True
            else:
                msg = 'Service unchanged'
            facts = new_service.get_facts()
    elif (module.params['state'] == 'absent'):
        msg = 'Service absent'
    else:
        if (not module.check_mode):
            service_id = self.create_service(module.params['name'], new_service)
        msg = 'Service created'
        changed = True
        facts = new_service.get_facts()
    return (msg, changed, rebuilt, changes, facts)
