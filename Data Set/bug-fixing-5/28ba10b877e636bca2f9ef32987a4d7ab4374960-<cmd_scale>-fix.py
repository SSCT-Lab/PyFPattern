def cmd_scale(self):
    result = dict(changed=False, actions=[])
    for service in self.project.services:
        if (service.name in self.scale):
            service_res = dict(service=service.name, scale=0)
            containers = service.containers(stopped=True)
            scale = self.parse_scale(service.name)
            if (len(containers) != scale):
                result['changed'] = True
                service_res['scale'] = (scale - len(containers))
                if (not self.check_mode):
                    try:
                        service.scale(scale)
                    except Exception as exc:
                        self.client.fail(('Error scaling %s - %s' % (service.name, str(exc))))
                result['actions'].append(service_res)
    return result