def extract_platform(self, host):
    try:
        return self.platforms_lookup[host['platform']['id']]
    except Exception:
        return