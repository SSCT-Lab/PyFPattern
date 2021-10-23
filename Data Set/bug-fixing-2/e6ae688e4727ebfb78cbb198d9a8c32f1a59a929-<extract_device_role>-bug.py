

def extract_device_role(self, host):
    try:
        return [self.device_roles_lookup[host['device_role']['id']]]
    except Exception:
        return
