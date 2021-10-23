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
    searchpath = [working_path]
    if (self._task._role is not None):
        searchpath.append(self._task._role._role_path)
        dep_chain = self._task._block.get_dep_chain()
        if (dep_chain is not None):
            for role in dep_chain:
                searchpath.append(role._role_path)
    searchpath.append(os.path.dirname(source))
    self._templar.environment.loader.searchpath = searchpath
    self._task.args['src'] = self._templar.template(template_data)