def parse(self, inventory, loader, path, cache=True):
    super(InventoryModule, self).parse(inventory, loader, path)
    path = os.path.abspath(path)
    cmd = [path, '--list']
    try:
        try:
            sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError as e:
            raise AnsibleError(('problem running %s (%s)' % (' '.join(cmd), e)))
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
            processed = self.loader.load(data)
        except Exception as e:
            raise AnsibleError('failed to parse executable inventory script results from {0}: {1}\n{2}'.format(path, to_native(e), err))
        if (not isinstance(processed, Mapping)):
            raise AnsibleError('failed to parse executable inventory script results from {0}: needs to be a json dict\n{1}'.format(path, err))
        group = None
        data_from_meta = None
        for (group, gdata) in data.items():
            if (group == '_meta'):
                if ('hostvars' in data):
                    data_from_meta = data['hostvars']
            else:
                self.parse_group(group, gdata)
        for host in self._hosts:
            got = {
                
            }
            if (data_from_meta is None):
                got = self.get_host_variables(path, host, data_from_meta)
            else:
                try:
                    got = data.get(host, {
                        
                    })
                except AttributeError as e:
                    raise AnsibleError(('Improperly formatted host information for %s: %s' % (host, to_native(e))))
                self.populate_host_vars(host, got, group)
    except Exception as e:
        raise AnsibleParserError(e)