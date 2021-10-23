def get_snippet_text(self, doc):
    text = []
    desc = CLI.tty_ify(doc['short_description'])
    text.append(('- name: %s' % desc))
    text.append(('  %s:' % doc['module']))
    pad = 31
    subdent = (' ' * pad)
    limit = (display.columns - pad)
    for o in sorted(doc['options'].keys()):
        opt = doc['options'][o]
        if isinstance(opt['description'], string_types):
            desc = CLI.tty_ify(opt['description'])
        else:
            desc = CLI.tty_ify(' '.join(opt['description']))
        required = opt.get('required', False)
        if (not isinstance(required, bool)):
            raise ("Incorrect value for 'Required', a boolean is needed.: %s" % required)
        if required:
            desc = ('(required) %s' % desc)
        o = ('%s:' % o)
        text.append(('      %-20s   # %s' % (o, textwrap.fill(desc, limit, subsequent_indent=subdent))))
    text.append('')
    return '\n'.join(text)