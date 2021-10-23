def _download_updates(self):
    updates_filename = 'jenkins-plugin-cache.json'
    updates_dir = os.path.expanduser('~/.ansible/tmp')
    updates_file = ('%s/%s' % (updates_dir, updates_filename))
    download_updates = True
    if os.path.isfile(updates_file):
        ts_file = os.stat(updates_file).st_mtime
        ts_now = time.time()
        if ((ts_now - ts_file) < self.params['updates_expiration']):
            download_updates = False
    updates_file_orig = updates_file
    if download_updates:
        url = ('%s/update-center.json' % self.params['updates_url'])
        r = self._get_url_data(url, msg_status='Remote updates not found.', msg_exception='Updates download failed.')
        updates_file = tempfile.mkstemp()
        try:
            fd = open(updates_file, 'wb')
        except IOError:
            e = get_exception()
            self.module.fail_json(msg=('Cannot open the tmp updates file %s.' % updates_file), details=str(e))
        fd.write(r.read())
        try:
            fd.close()
        except IOError:
            e = get_exception()
            self.module.fail_json(msg=('Cannot close the tmp updates file %s.' % updates_file), detail=str(e))
    try:
        f = open(updates_file)
    except IOError:
        e = get_exception()
        self.module.fail_json(msg='Cannot open temporal updates file.', details=str(e))
    i = 0
    for line in f:
        if (i == 1):
            try:
                data = json.loads(line)
            except Exception:
                e = get_exception()
                self.module.fail_json(msg='Cannot load JSON data from the tmp updates file.', details=e.message)
            break
        i += 1
    if download_updates:
        if (not os.path.isdir(updates_dir)):
            try:
                os.makedirs(updates_dir, int('0700', 8))
            except OSError:
                e = get_exception()
                self.module.fail_json(msg='Cannot create temporal directory.', details=e.message)
        self.module.atomic_move(updates_file, updates_file_orig)
    if (('plugins' not in data) or (self.params['name'] not in data['plugins'])):
        self.module.fail_json(msg='Cannot find plugin data in the updates file.')
    return data['plugins'][self.params['name']]