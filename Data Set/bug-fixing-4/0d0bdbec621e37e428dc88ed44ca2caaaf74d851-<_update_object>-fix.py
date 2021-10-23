def _update_object(self, obj, name, path):
    setattr(obj, '_original_path', path)
    setattr(obj, '_load_name', name)