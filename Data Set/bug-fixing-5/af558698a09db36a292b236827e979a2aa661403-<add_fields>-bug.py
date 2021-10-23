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
            choices = (('(Aliases: ' + ', '.join((str(i) for i in opt['aliases']))) + ')')
            del opt['aliases']
        choices = ''
        if ('choices' in opt):
            choices = (('(Choices: ' + ', '.join((str(i) for i in opt['choices']))) + ')')
            del opt['choices']
        default = ''
        if (('default' in opt) or (not required)):
            default = (('[Default: ' + str(opt.pop('default', '(null)'))) + ']')
        text.append(textwrap.fill(CLI.tty_ify(((aliases + choices) + default)), limit, initial_indent=opt_indent, subsequent_indent=opt_indent))
        if ('options' in opt):
            text.append((opt_indent + 'options:\n'))
            self.add_fields(text, opt['options'], limit, (opt_indent + opt_indent))
            text.append('')
            del opt['options']
        if ('spec' in opt):
            text.append((opt_indent + 'spec:\n'))
            self.add_fields(text, opt['spec'], limit, (opt_indent + opt_indent))
            text.append('')
            del opt['spec']
        for conf in ('config', 'env_vars', 'host_vars'):
            if (conf in opt):
                text.append(textwrap.fill(CLI.tty_ify(('%s: ' % conf)), limit, initial_indent=opt_indent, subsequent_indent=opt_indent))
                for entry in opt[conf]:
                    if isinstance(entry, dict):
                        pre = '  -'
                        for key in entry:
                            text.append(textwrap.fill(CLI.tty_ify(('%s %s: %s' % (pre, key, entry[key]))), limit, initial_indent=opt_indent, subsequent_indent=opt_indent))
                            pre = '   '
                    else:
                        text.append(textwrap.fill(CLI.tty_ify(('  - %s' % entry)), limit, initial_indent=opt_indent, subsequent_indent=opt_indent))
                del opt[conf]
        for k in opt:
            if k.startswith('_'):
                continue
            if isinstance(opt[k], string_types):
                text.append(textwrap.fill(CLI.tty_ify(('%s: %s' % (k, opt[k]))), limit, initial_indent=opt_indent, subsequent_indent=opt_indent))
            elif isinstance(opt[k], (list, dict)):
                text.append(textwrap.fill(CLI.tty_ify(('%s: %s' % (k, yaml.dump(opt[k], Dumper=AnsibleDumper, default_flow_style=False)))), limit, initial_indent=opt_indent, subsequent_indent=opt_indent))
            else:
                display.vv(("Skipping %s key cuase we don't know how to handle eet" % k))