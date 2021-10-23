def _find_vars_files(self, path, name):
    ' Find {group,host}_vars files '
    b_path = to_bytes(os.path.join(path, name))
    found = []
    for ext in (C.YAML_FILENAME_EXTENSIONS + ['']):
        if ('.' in ext):
            full_path = (b_path + to_bytes(ext))
        elif ext:
            full_path = b'.'.join([b_path, to_bytes(ext)])
        else:
            full_path = b_path
        if os.path.exists(full_path):
            self._display.debug(('\tfound %s' % to_text(full_path)))
            if os.path.isdir(full_path):
                for spath in os.listdir(full_path):
                    if os.path.isdir(spath):
                        found.extend(self._find_vars_files(spath, name))
                    else:
                        found.append(spath)
            else:
                found.append(full_path)
    return found