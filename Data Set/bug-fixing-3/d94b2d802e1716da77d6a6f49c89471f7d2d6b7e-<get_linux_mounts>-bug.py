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
            'root': fields[3],
            'dst': fields[4],
            'opts': fields[5],
            'fields': fields[6:(- 4)],
            'fs': fields[(- 3)],
            'src': fields[(- 2)],
        }
        mntinfo.append(record)
    mounts = {
        
    }
    for (i, mnt) in enumerate(mntinfo):
        src = mnt['src']
        if ((mnt['fs'] == 'tmpfs') and (mnt['root'] != '/')):
            shared = None
            for fld in mnt['fields']:
                if fld.startswith('shared'):
                    shared = fld
            if (shared is None):
                continue
            dest = None
            for (j, m) in enumerate(mntinfo):
                if (j < i):
                    if (shared in m['fields']):
                        dest = m['dst']
                else:
                    break
            if (dest is not None):
                src = ('%s%s' % (dest, mnt['root']))
            else:
                continue
        elif ((mnt['root'] != '/') and (len(mnt['fields']) > 0)):
            for (j, m) in enumerate(mntinfo):
                if (j < i):
                    if (m['src'] == mnt['src']):
                        src = ('%s%s' % (m['dst'], mnt['root']))
                else:
                    break
        elif ((mnt['root'] != '/') and (len(mnt['fields']) == 0)):
            src = mnt['root']
            for (j, m) in enumerate(mntinfo):
                if (j < i):
                    if ((m['src'] == mnt['src']) and mnt['root'].startswith(m['root'])):
                        src = src.replace(('%s/' % m['root']), '/', 1)
                else:
                    break
        mounts[mnt['dst']] = {
            'src': src,
            'opts': mnt['opts'],
            'fs': mnt['fs'],
        }
    return mounts