def get_linux_mounts(module):
    'Gather mount information'
    mntinfo_file = '/proc/self/mountinfo'
    try:
        f = open(mntinfo_file)
    except IOError:
        return
    lines = map(str.strip, f.readlines())
    try:
        f.close()
    except IOError:
        module.fail_json(msg=('Cannot close file %s' % mntinfo_file))
    mntinfo = []
    for line in lines:
        fields = line.split()
        record = {
            'id': int(fields[0]),
            'parent_id': int(fields[1]),
            'root': fields[3],
            'dst': fields[4],
            'opts': fields[5],
            'fs': fields[(- 3)],
            'src': fields[(- 2)],
        }
        mntinfo.append(record)
    mounts = {
        
    }
    for mnt in mntinfo:
        src = mnt['src']
        if (mnt['parent_id'] != 1):
            for m in mntinfo:
                if (mnt['parent_id'] == m['id']):
                    if ((len(m['root']) > 1) and mnt['root'].startswith(('%s/' % m['root']))):
                        mnt['root'] = mnt['root'][(len(m['root']) + 1):]
                    if (m['dst'] != '/'):
                        mnt['root'] = ('%s%s' % (m['dst'], mnt['root']))
                    src = mnt['root']
                    break
        mounts[mnt['dst']] = {
            'src': src,
            'opts': mnt['opts'],
            'fs': mnt['fs'],
        }
    return mounts