def extract_config_context(self, host):
    try:
        return [host['config_context']]
    except Exception:
        return