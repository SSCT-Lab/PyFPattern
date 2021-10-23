def __init__(self):
    super(ImportFeedsPlugin, self).__init__()
    self.config.add({
        'formats': [],
        'm3u_name': 'imported.m3u',
        'dir': None,
        'relative_to': None,
        'absolute_path': False,
    })
    feeds_dir = self.config['dir'].get()
    if feeds_dir:
        feeds_dir = os.path.expanduser(bytestring_path(feeds_dir))
        self.config['dir'] = feeds_dir
        if (not os.path.exists(syspath(feeds_dir))):
            os.makedirs(syspath(feeds_dir))
    relative_to = self.config['relative_to'].get()
    if relative_to:
        self.config['relative_to'] = normpath(relative_to)
    else:
        self.config['relative_to'] = feeds_dir
    self.register_listener('library_opened', self.library_opened)
    self.register_listener('album_imported', self.album_imported)
    self.register_listener('item_imported', self.item_imported)