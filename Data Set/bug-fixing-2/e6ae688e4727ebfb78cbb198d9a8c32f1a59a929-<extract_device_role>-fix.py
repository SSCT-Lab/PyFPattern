

def extract_device_role(self, host):
    try:
        if ('device_role' in host):
            return [self.device_roles_lookup[host['device_role']['id']]]
        elif ('role' in host):
            return [self.device_roles_lookup[host['role']['id']]]
    except Exception:
        return
