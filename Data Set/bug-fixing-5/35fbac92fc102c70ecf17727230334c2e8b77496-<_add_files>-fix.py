def _add_files(self, path, parent=None):
    path = expanduser(path)
    if isfile(path):
        path = dirname(path)
    files = []
    fappend = files.append
    for f in self.file_system.listdir(path):
        try:
            fappend(normpath(join(path, f)))
        except UnicodeDecodeError:
            Logger.exception('unable to decode <{}>'.format(f))
        except UnicodeEncodeError:
            Logger.exception('unable to encode <{}>'.format(f))
    files = self._apply_filters(files)
    files = self.sort_func(files, self.file_system)
    is_hidden = self.file_system.is_hidden
    if (not self.show_hidden):
        files = [x for x in files if (not is_hidden(x))]
    self.files[:] = files
    total = len(files)
    wself = ref(self)
    for (index, fn) in enumerate(files):

        def get_nice_size():
            return self.get_nice_size(fn)
        ctx = {
            'name': basename(fn),
            'get_nice_size': get_nice_size,
            'path': fn,
            'controller': wself,
            'isdir': self.file_system.is_dir(fn),
            'parent': parent,
            'sep': sep,
        }
        entry = self._create_entry_widget(ctx)
        (yield (index, total, entry))