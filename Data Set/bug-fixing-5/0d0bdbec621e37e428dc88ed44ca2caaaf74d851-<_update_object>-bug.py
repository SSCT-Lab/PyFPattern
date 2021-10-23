def _update_object(self, obj, name, path):
    self._load_config_defs(name, path)
    setattr(obj, '_original_path', path)
    setattr(obj, '_load_name', name)