def _parse(self, path, lines):
    '\n        Populates self.groups from the given array of lines. Raises an error on\n        any parse failure.\n        '
    self._compile_patterns()
    pending_declarations = {
        
    }
    groupname = 'ungrouped'
    state = 'hosts'
    self.lineno = 0
    for line in lines:
        self.lineno += 1
        line = line.strip()
        if ((not line) or (line[0] in self._COMMENT_MARKERS)):
            continue
        m = self.patterns['section'].match(line)
        if m:
            (groupname, state) = m.groups()
            state = (state or 'hosts')
            if (state not in ['hosts', 'children', 'vars']):
                title = ':'.join(m.groups())
                self._raise_error(('Section [%s] has unknown type: %s' % (title, state)))
            self.inventory.add_group(groupname)
            if (state == 'vars'):
                pending_declarations[groupname] = dict(line=self.lineno, state=state, name=groupname)
            if ((groupname in pending_declarations) and (state != 'vars')):
                if (pending_declarations[groupname]['state'] == 'children'):
                    self._add_pending_children(groupname, pending_declarations)
            continue
        elif (line.startswith('[') and line.endswith(']')):
            self._raise_error((("Invalid section entry: '%s'. Please make sure that there are no spaces" % line) + 'in the section entry, and that there are no other invalid characters'))
        if (state == 'hosts'):
            (hosts, port, variables) = self._parse_host_definition(line)
            self.populate_host_vars(hosts, variables, groupname, port)
        elif (state == 'vars'):
            (k, v) = self._parse_variable_definition(line)
            self.inventory.set_variable(groupname, k, v)
        elif (state == 'children'):
            child = self._parse_group_name(line)
            if (child not in self.inventory.groups):
                if (child not in pending_declarations):
                    pending_declarations[child] = dict(line=self.lineno, state=state, name=child, parents=[groupname])
                else:
                    pending_declarations[child]['parents'].append(groupname)
            else:
                self.inventory.add_child(groupname, child)
        else:
            self._raise_error(('Entered unhandled state: %s' % state))
    for g in pending_declarations:
        if (g not in self.inventory.groups):
            decl = pending_declarations[g]
            if (decl['state'] == 'vars'):
                raise AnsibleError(('%s:%d: Section [%s:vars] not valid for undefined group: %s' % (path, decl['line'], decl['name'], decl['name'])))
            elif (decl['state'] == 'children'):
                raise AnsibleError(('%s:%d: Section [%s:children] includes undefined group: %s' % (path, decl['line'], decl['parents'].pop(), decl['name'])))