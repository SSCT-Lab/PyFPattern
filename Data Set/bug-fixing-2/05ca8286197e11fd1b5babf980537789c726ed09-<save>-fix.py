

def save(self):
    for (filename, sources) in list(self.files.items()):
        if sources:
            (d, fn) = os.path.split(filename)
            try:
                os.makedirs(d)
            except OSError as err:
                if (not os.path.isdir(d)):
                    self.module.fail_json(('Failed to create directory %s: %s' % (d, to_native(err))))
            (fd, tmp_path) = tempfile.mkstemp(prefix=('.%s-' % fn), dir=d)
            f = os.fdopen(fd, 'w')
            for (n, valid, enabled, source, comment) in sources:
                chunks = []
                if (not enabled):
                    chunks.append('# ')
                chunks.append(source)
                if comment:
                    chunks.append(' # ')
                    chunks.append(comment)
                chunks.append('\n')
                line = ''.join(chunks)
                try:
                    f.write(line)
                except IOError as err:
                    self.module.fail_json(msg=('Failed to write to file %s: %s' % (tmp_path, to_native(err))))
            self.module.atomic_move(tmp_path, filename)
            if (filename in self.new_repos):
                this_mode = self.module.params.get('mode', DEFAULT_SOURCES_PERM)
                self.module.set_mode_if_different(filename, this_mode, False)
        else:
            del self.files[filename]
            if os.path.exists(filename):
                os.remove(filename)
