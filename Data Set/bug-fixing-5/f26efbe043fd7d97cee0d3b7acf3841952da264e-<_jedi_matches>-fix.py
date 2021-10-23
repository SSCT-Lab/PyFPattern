def _jedi_matches(self, cursor_column: int, cursor_line: int, text: str):
    '\n\n        Return a list of :any:`jedi.api.Completions` object from a ``text`` and\n        cursor position.\n\n        Parameters\n        ----------\n        cursor_column : int\n            column position of the cursor in ``text``, 0-indexed.\n        cursor_line : int\n            line position of the cursor in ``text``, 0-indexed\n        text : str\n            text to complete\n\n        Debugging\n        ---------\n\n        If ``IPCompleter.debug`` is ``True`` may return a :any:`_FakeJediCompletion`\n        object containing a string with the Jedi debug information attached.\n        '
    namespaces = [self.namespace]
    if (self.global_namespace is not None):
        namespaces.append(self.global_namespace)
    completion_filter = (lambda x: x)
    offset = cursor_to_position(text, cursor_line, cursor_column)
    if offset:
        pre = text[(offset - 1)]
        if (pre == '.'):
            if (self.omit__names == 2):
                completion_filter = (lambda c: (not c.name.startswith('_')))
            elif (self.omit__names == 1):
                completion_filter = (lambda c: (not (c.name.startswith('__') and c.name.endswith('__'))))
            elif (self.omit__names == 0):
                completion_filter = (lambda x: x)
            else:
                raise ValueError("Don't understand self.omit__names == {}".format(self.omit__names))
    interpreter = jedi.Interpreter(text, namespaces, column=cursor_column, line=(cursor_line + 1))
    try_jedi = True
    try:
        try:
            from jedi.parser.tree import ErrorLeaf
        except ImportError:
            from parso.tree import ErrorLeaf
        next_to_last_tree = interpreter._get_module().tree_node.children[(- 2)]
        completing_string = False
        if isinstance(next_to_last_tree, ErrorLeaf):
            completing_string = (next_to_last_tree.value.lstrip()[0] in {'"', "'"})
        try_jedi = (not completing_string)
    except Exception as e:
        if self.debug:
            print('Error detecting if completing a non-finished string :', e, '|')
    if (not try_jedi):
        return []
    try:
        return filter(completion_filter, interpreter.completions())
    except Exception as e:
        if self.debug:
            return [_FakeJediCompletion(('Oops Jedi has crashed, please report a bug with the following:\n"""\n%s\ns"""' % e))]
        else:
            return []