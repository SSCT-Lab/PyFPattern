

def _handle_template(self):
    src = self._task.args.get('src')
    working_path = self._get_working_path()
    if (os.path.isabs(src) or urlparse.urlsplit('src').scheme):
        source = src
    else:
        source = self._loader.path_dwim_relative(working_path, 'templates', src)
        if (not source):
            source = self._loader.path_dwim_relative(working_path, src)
    if (not os.path.exists(source)):
        return
    try:
        with open(source, 'r') as f:
            template_data = to_unicode(f.read())
    except IOError:
        return dict(failed=True, msg='unable to load src file')
    self._task.args['src'] = self._templar.template(template_data)
