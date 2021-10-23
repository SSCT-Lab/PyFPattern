def _return_formatted(self, kwargs):
    self.add_path_info(kwargs)
    if ('invocation' not in kwargs):
        kwargs['invocation'] = {
            'module_args': self.params,
        }
    if ('warnings' in kwargs):
        if isinstance(kwargs['warnings'], list):
            for w in kwargs['warnings']:
                self.warn(w)
        else:
            self.warn(kwargs['warnings'])
    if self._warnings:
        kwargs['warnings'] = self._warnings
    if ('deprecations' in kwargs):
        if isinstance(kwargs['deprecations'], list):
            for d in kwargs['deprecations']:
                if (isinstance(d, SEQUENCETYPE) and (len(d) == 2)):
                    self.deprecate(d[0], version=d[1])
                else:
                    self.deprecate(d)
        else:
            self.deprecate(kwargs['deprecations'])
    if self._deprecations:
        kwargs['deprecations'] = self._deprecations
    kwargs = remove_values(kwargs, self.no_log_values)
    print(('\n%s' % self.jsonify(kwargs)))