def get_snippet_text(self, doc):
    text = []
    desc = CLI.tty_ify(doc['short_description'])
    text.append(('- name: %s' % desc))
    text.append(('  action: %s' % doc['module']))
    pad = 31
    subdent = (' ' * pad)
    limit = (display.columns - pad)
    for o in sorted(doc['options'].keys()):
        opt = doc['options'][o]
        desc = CLI.tty_ify(' '.join(opt['description']))
        required = opt.get('required', False)
        if (not isinstance(required, bool)):
            raise ("Incorrect value for 'Required', a boolean is needed.: %s" % required)
        if required:
            s = (o + '=')
        else:
            s = o
        text.append(('      %-20s   # %s' % (s, textwrap.fill(desc, limit, subsequent_indent=subdent))))
    text.append('')
    return '\n'.join(text)