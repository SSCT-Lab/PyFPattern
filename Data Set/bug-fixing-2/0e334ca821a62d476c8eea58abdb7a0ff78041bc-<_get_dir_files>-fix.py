

def _get_dir_files(self, path):
    found = []
    for spath in os.listdir(path):
        if ((not spath.startswith('.')) and (not spath.endswith('~'))):
            ext = os.path.splitext(spath)[(- 1)]
            full_spath = os.path.join(path, spath)
            if (os.path.isdir(full_spath) and (not ext)):
                found.extend(self._get_dir_files(full_spath))
            elif (os.path.isfile(full_spath) and ((not ext) or (to_text(ext) in C.YAML_FILENAME_EXTENSIONS))):
                found.append(full_spath)
    return found
