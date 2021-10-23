def _needs_to_change_container_config(self, key):
    if (key not in self.config):
        return False
    if (key == 'config'):
        old_configs = dict(((k, v) for (k, v) in self.old_container_json['metadata'][key].items() if (not k.startswith('volatile.'))))
        for (k, v) in self.config['config'].items():
            if (k not in old_configs):
                return True
            if (old_configs[k] != v):
                return True
        return False
    else:
        old_configs = self.old_container_json['metadata'][key]
        return (self.config[key] != old_configs)