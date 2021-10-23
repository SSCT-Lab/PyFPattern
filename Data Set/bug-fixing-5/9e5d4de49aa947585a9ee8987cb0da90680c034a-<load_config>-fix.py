def load_config(self, config, commit=False, replace=False, confirm=None, comment=None, config_format='text', overwrite=False):
    if all([replace, overwrite]):
        self.raise_exc('setting both replace and overwrite to True is invalid')
    if replace:
        merge = False
        overwrite = False
    elif overwrite:
        merge = False
        overwrite = True
    else:
        merge = True
        overwrite = False
    if (overwrite and (config_format == 'set')):
        self.raise_exc('replace cannot be True when config_format is `set`')
    self.lock_config()
    try:
        candidate = '\n'.join(config)
        self.config.load(candidate, format=config_format, merge=merge, overwrite=overwrite)
    except ConfigLoadError:
        exc = get_exception()
        self.raise_exc(('Unable to load config: %s' % str(exc)))
    diff = self.config.diff()
    self.check_config()
    if all((commit, diff)):
        self.commit_config(comment=comment, confirm=confirm)
    self.unlock_config()
    return diff