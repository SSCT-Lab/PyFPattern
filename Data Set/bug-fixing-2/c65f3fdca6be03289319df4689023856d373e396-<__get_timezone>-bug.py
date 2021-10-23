

def __get_timezone(self):
    zoneinfo_dir = '/usr/share/zoneinfo/'
    localtime_file = '/etc/localtime'
    if (not os.path.exists(localtime_file)):
        self.module.warn('Could not read /etc/localtime. Assuming UTC.')
        return 'UTC'
    planned = self.value['name']['planned']
    try:
        already_planned_state = filecmp.cmp(os.path.join(zoneinfo_dir, planned), localtime_file)
    except OSError:
        already_planned_state = False
    if already_planned_state:
        return planned
    zoneinfo_file = localtime_file
    while (not zoneinfo_file.startswith(zoneinfo_dir)):
        try:
            zoneinfo_file = os.readlink(localtime_file)
        except OSError:
            break
    else:
        return zoneinfo_file.replace(zoneinfo_dir, '')
    for (dname, _, fnames) in os.walk(zoneinfo_dir):
        for fname in fnames:
            zoneinfo_file = os.path.join(dname, fname)
            if filecmp.cmp(zoneinfo_file, localtime_file):
                return zoneinfo_file.replace(zoneinfo_dir, '')
    self.module.warn('Could not identify timezone name from /etc/localtime. Assuming UTC.')
    return 'UTC'
