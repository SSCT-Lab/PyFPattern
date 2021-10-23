def add_fields(self, text, fields, limit, opt_indent):
    for o in sorted(fields):
        opt = fields[o]
        required = opt.pop('required', False)
        if (not isinstance(required, bool)):
            raise AnsibleError(("Incorrect value for 'Required', a boolean is needed.: %s" % required))
        if required:
            opt_leadin = '='
        else:
            opt_leadin = '-'
        text.append(('%s %s' % (opt_leadin, o)))
        if isinstance(opt['description'], list):
            for entry in opt['description']:
                text.append(textwrap.fill(CLI.tty_ify(entry), limit, initial_indent=opt_indent, subsequent_indent=opt_indent))
        else:
            text.append(textwrap.fill(CLI.tty_ify(opt['description']), limit, initial_indent=opt_indent, subsequent_indent=opt_indent))
        del opt['description']
        aliases = ''
        if ('aliases' in opt):
            if (len(opt['aliases']) > 0):
                aliases = (('(Aliases: ' + ', '.join((str(i) for i in opt['aliases']))) + ')')
            del opt['aliases']
        choices = ''
        if ('choices' in opt):
            if (len(opt['choices']) > 0):
                choices = (('(Choices: ' + ', '.join((str(i) for i in opt['choices']))) + ')')
            del opt['choices']
        default = ''
        if (('default' in opt) or (not required)):
            default = (('[Default: %s' % str(opt.pop('default', '(null)'))) + ']')
        text.append(textwrap.fill(CLI.tty_ify(((aliases + choices) + default)), limit, initial_indent=opt_indent, subsequent_indent=opt_indent))
        if ('options' in opt):
            text.append(('%soptions:\n' % opt_indent))
            self.add_fields(text, opt.pop('options'), limit, (opt_indent + opt_indent))
        if ('spec' in opt):
            text.append(('%sspec:\n' % opt_indent))
            self.add_fields(text, opt.pop('spec'), limit, (opt_indent + opt_indent))
        conf = {
            
        }
        for config in ('env', 'ini', 'yaml', 'vars'):
            if ((config in opt) and opt[config]):
                conf[config] = opt.pop(config)
                for ignore in self.IGNORE:
                    for item in conf[config]:
                        if (ignore in item):
                            del item[ignore]
        if conf:
            text.append(self._dump_yaml({
                'set_via': conf,
            }, opt_indent))
        for k in sorted(opt):
            if k.startswith('_'):
                continue
            if isinstance(opt[k], string_types):
                text.append(('%s%s: %s' % (opt_indent, k, textwrap.fill(CLI.tty_ify(opt[k]), (limit - (len(k) + 2)), subsequent_indent=opt_indent))))
            elif isinstance(opt[k], (list, tuple)):
                text.append(CLI.tty_ify(('%s%s: %s' % (opt_indent, k, ', '.join(opt[k])))))
            else:
                text.append(self._dump_yaml({
                    k: opt[k],
                }, opt_indent))
        text.append('')