def __init__(self):
    super(ImportFeedsPlugin, self).__init__()
    self.config.add({
        'formats': [],
        'm3u_name': 'imported.m3u',
        'dir': None,
        'relative_to': None,
        'absolute_path': False,
    })
    relative_to = self.config['relative_to'].get()
    if relative_to:
        self.config['relative_to'] = normpath(relative_to)
    else:
        self.config['relative_to'] = self.get_feeds_dir()
    self.register_listener('album_imported', self.album_imported)
    self.register_listener('item_imported', self.item_imported)