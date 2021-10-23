def verify_file(self, path):
    valid = False
    if super(InventoryModule, self).verify_file(path):
        (file_name, ext) = os.path.splitext(path)
        if ((not ext) or (ext in C.YAML_FILENAME_EXTENSIONS)):
            valid = True
    return valid