def cmd_scale(self):
    result = dict(changed=False, actions=[])
    for service in self.project.services:
        if (service.name in self.scale):
            service_res = dict(service=service.name, scale=0)
            containers = service.containers(stopped=True)
            if (len(containers) != self.scale[service.name]):
                result['changed'] = True
                service_res['scale'] = (self.scale[service.name] - len(containers))
                if (not self.check_mode):
                    try:
                        service.scale(int(self.scale[service.name]))
                    except Exception as exc:
                        self.client.fail(('Error scaling %s - %s' % (service.name, str(exc))))
                result['actions'].append(service_res)
    return result