

def create(self):
    if self.module.check_mode:
        self.changed = True
        return
    properties = self.properties
    volsize = properties.pop('volsize', None)
    volblocksize = properties.pop('volblocksize', None)
    origin = properties.pop('origin', None)
    cmd = [self.zfs_cmd]
    if ('@' in self.name):
        action = 'snapshot'
    elif origin:
        action = 'clone'
    else:
        action = 'create'
    cmd.append(action)
    if (action in ['create', 'clone']):
        cmd += ['-p']
    if volsize:
        cmd += ['-V', volsize]
    if volblocksize:
        cmd += ['-b', volblocksize]
    if properties:
        for (prop, value) in properties.items():
            cmd += ['-o', ('%s="%s"' % (prop, value))]
    if origin:
        cmd.append(origin)
    cmd.append(self.name)
    (rc, out, err) = self.module.run_command(' '.join(cmd))
    if (rc == 0):
        self.changed = True
    else:
        self.module.fail_json(msg=err)
