def get_vars(self, loader, path, entities, cache=True):
    ' parses the inventory file '
    if (not isinstance(entities, list)):
        entities = [entities]
    super(VarsModule, self).get_vars(loader, path, entities)
    data = {
        
    }
    for entity in entities:
        if isinstance(entity, Host):
            subdir = 'host_vars'
        elif isinstance(entity, Group):
            subdir = 'group_vars'
        else:
            raise AnsibleParserError(('Supplied entity must be Host or Group, got %s instead' % type(entity)))
        if (not entity.name.startswith(os.path.sep)):
            try:
                found_files = []
                opath = os.path.realpath(os.path.join(self._basedir, subdir))
                key = ('%s.%s' % (entity.name, opath))
                if (cache and (key in FOUND)):
                    found_files = FOUND[key]
                else:
                    b_opath = to_bytes(opath)
                    if os.path.exists(b_opath):
                        if os.path.isdir(b_opath):
                            self._display.debug(('\tprocessing dir %s' % opath))
                            found_files = self._find_vars_files(opath, entity.name)
                            FOUND[key] = found_files
                        else:
                            self._display.warning(('Found %s that is not a directory, skipping: %s' % (subdir, opath)))
                for found in found_files:
                    new_data = loader.load_from_file(found, cache=True, unsafe=True)
                    if new_data:
                        data = combine_vars(data, new_data)
            except Exception as e:
                raise AnsibleParserError(to_native(e))
    return data