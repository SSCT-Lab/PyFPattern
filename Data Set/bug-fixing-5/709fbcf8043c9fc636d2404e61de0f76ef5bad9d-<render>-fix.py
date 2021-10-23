def render(self, config=None):
    commands = list()
    existing_as = None
    if config:
        match = re.search('router bgp (\\d+)', config, re.M)
        if match:
            existing_as = match.group(1)
    operation = self.params['operation']
    context = None
    if self.params['config']:
        context = ('router bgp %s' % self.get_value('config.bgp_as'))
    if (operation == 'delete'):
        if existing_as:
            commands.append(('no router bgp %s' % existing_as))
        elif context:
            commands.append(('no %s' % context))
    else:
        self._validate_input(config)
        if (operation == 'replace'):
            if (existing_as and (int(existing_as) != self.get_value('config.bgp_as'))):
                commands.append(('no router bgp %s' % existing_as))
                config = None
        elif (operation == 'override'):
            if existing_as:
                commands.append(('no router bgp %s' % existing_as))
            config = None
        context_commands = list()
        for (key, value) in iteritems(self.get_value('config')):
            if (value is not None):
                meth = getattr(self, ('_render_%s' % key), None)
                if meth:
                    resp = meth(config)
                    if resp:
                        context_commands.extend(to_list(resp))
        if (context and context_commands):
            commands.append(context)
            commands.extend(context_commands)
            commands.append('exit')
    return commands