def parse(self, inventory, loader, path, cache=True):
    super(InventoryModule, self).parse(inventory, loader, path)
    cmd = [path, '--list']
    try:
        cache_key = self.get_cache_prefix(path)
        if ((not cache) or (cache_key not in inventory.cache)):
            try:
                sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except OSError as e:
                raise AnsibleParserError(('problem running %s (%s)' % (' '.join(cmd), to_native(e))))
            (stdout, stderr) = sp.communicate()
            path = to_native(path)
            if stderr:
                err = (to_native(stderr) + '\n')
            if (sp.returncode != 0):
                raise AnsibleError(('Inventory script (%s) had an execution error: %s ' % (path, err)))
            try:
                data = to_text(stdout, errors='strict')
            except Exception as e:
                raise AnsibleError('Inventory {0} contained characters that cannot be interpreted as UTF-8: {1}'.format(path, to_native(e)))
            try:
                inventory.cache[cache_key] = self.loader.load(data, file_name=path)
            except Exception as e:
                raise AnsibleError('failed to parse executable inventory script results from {0}: {1}\n{2}'.format(path, to_native(e), err))
        processed = inventory.cache[cache_key]
        if (not isinstance(processed, Mapping)):
            raise AnsibleError('failed to parse executable inventory script results from {0}: needs to be a json dict\n{1}'.format(path, err))
        group = None
        data_from_meta = None
        for (group, gdata) in processed.items():
            if (group == '_meta'):
                if ('hostvars' in gdata):
                    data_from_meta = gdata['hostvars']
            else:
                self._parse_group(group, gdata)
        for host in self._hosts:
            got = {
                
            }
            if (data_from_meta is None):
                got = self.get_host_variables(path, host)
            else:
                try:
                    got = data_from_meta.get(host, {
                        
                    })
                except AttributeError as e:
                    raise AnsibleError(('Improperly formatted host information for %s: %s' % (host, to_native(e))))
            self.populate_host_vars([host], got)
    except Exception as e:
        raise AnsibleParserError(to_native(e))