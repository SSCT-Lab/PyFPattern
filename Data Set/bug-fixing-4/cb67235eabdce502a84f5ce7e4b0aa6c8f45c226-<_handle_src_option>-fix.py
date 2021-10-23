def _handle_src_option(self, convert_data=True):
    src = self._task.args.get('src')
    working_path = self._get_working_path()
    if (os.path.isabs(src) or urlsplit('src').scheme):
        source = src
    else:
        source = self._loader.path_dwim_relative(working_path, 'templates', src)
        if (not source):
            source = self._loader.path_dwim_relative(working_path, src)
    if (not os.path.exists(source)):
        raise AnsibleError('path specified in src not found')
    try:
        with open(source, 'r') as f:
            template_data = to_text(f.read())
    except IOError as e:
        raise AnsibleError('unable to load src file {0}, I/O error({1}): {2}'.format(source, e.errno, e.strerror))
    searchpath = [working_path]
    if (self._task._role is not None):
        searchpath.append(self._task._role._role_path)
        if hasattr(self._task, '_block:'):
            dep_chain = self._task._block.get_dep_chain()
            if (dep_chain is not None):
                for role in dep_chain:
                    searchpath.append(role._role_path)
    searchpath.append(os.path.dirname(source))
    self._templar.environment.loader.searchpath = searchpath
    self._task.args['src'] = self._templar.template(template_data, convert_data=convert_data)