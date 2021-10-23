def _record_items(self, lib, basename, items):
    'Records relative paths to the given items for each feed format\n        '
    feedsdir = bytestring_path(self.config['dir'].as_filename())
    formats = self.config['formats'].as_str_seq()
    relative_to = (self.config['relative_to'].get() or self.config['dir'].as_filename())
    relative_to = bytestring_path(relative_to)
    paths = []
    for item in items:
        if self.config['absolute_path']:
            paths.append(item.path)
        else:
            try:
                relpath = os.path.relpath(item.path, relative_to)
            except ValueError:
                relpath = item.path
            paths.append(relpath)
    if ('m3u' in formats):
        m3u_basename = bytestring_path(self.config['m3u_name'].as_str())
        m3u_path = os.path.join(feedsdir, m3u_basename)
        _write_m3u(m3u_path, paths)
    if ('m3u_multi' in formats):
        m3u_path = _build_m3u_filename(basename)
        _write_m3u(m3u_path, paths)
    if ('link' in formats):
        for path in paths:
            dest = os.path.join(feedsdir, os.path.basename(path))
            if (not os.path.exists(syspath(dest))):
                link(path, dest)
    if ('echo' in formats):
        self._log.info('Location of imported music:')
        for path in paths:
            self._log.info('  {0}', path)