

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
        (update_fd, updates_file) = tempfile.mkstemp()
        os.write(update_fd, r.read())
        try:
            os.close(update_fd)
        except IOError as e:
            self.module.fail_json(msg=('Cannot close the tmp updates file %s.' % updates_file), details=to_native(e))
    try:
        f = open(updates_file, encoding='utf-8')
    except IOError as e:
        self.module.fail_json(msg='Cannot open temporal updates file.', details=to_native(e))
    i = 0
    for line in f:
        if (i == 1):
            try:
                data = json.loads(line)
            except Exception as e:
                self.module.fail_json(msg='Cannot load JSON data from the tmp updates file.', details=to_native(e))
            break
        i += 1
    if download_updates:
        if (not os.path.isdir(updates_dir)):
            try:
                os.makedirs(updates_dir, int('0700', 8))
            except OSError as e:
                self.module.fail_json(msg='Cannot create temporal directory.', details=to_native(e))
        self.module.atomic_move(updates_file, updates_file_orig)
    if (('plugins' not in data) or (self.params['name'] not in data['plugins'])):
        self.module.fail_json(msg='Cannot find plugin data in the updates file.')
    return data['plugins'][self.params['name']]
