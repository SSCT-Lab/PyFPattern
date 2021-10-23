def create(self):
    if self.module.check_mode:
        self.changed = True
        return
    properties = self.properties
    origin = self.module.params.get('origin', None)
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
    if properties:
        for (prop, value) in properties.items():
            if (prop == 'volsize'):
                cmd += ['-V', value]
            elif (prop == 'volblocksize'):
                cmd += ['-b', value]
            else:
                cmd += ['-o', ('%s="%s"' % (prop, value))]
    if (origin and (action == 'clone')):
        cmd.append(origin)
    cmd.append(self.name)
    (rc, out, err) = self.module.run_command(' '.join(cmd))
    if (rc == 0):
        self.changed = True
    else:
        self.module.fail_json(msg=err)