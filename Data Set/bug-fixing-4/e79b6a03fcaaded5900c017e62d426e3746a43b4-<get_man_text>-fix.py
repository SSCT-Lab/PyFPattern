def get_man_text(self, doc):
    IGNORE = frozenset(['module', 'docuri', 'version_added', 'short_description', 'now_date', 'plainexamples', 'returndocs'])
    opt_indent = '        '
    text = []
    pad = (display.columns * 0.2)
    limit = max((display.columns - int(pad)), 70)
    text.append(('> %s    (%s)\n' % (doc.get(self.options.type, doc.get('plugin_type')).upper(), doc.pop('filename'))))
    if isinstance(doc['description'], list):
        desc = ' '.join(doc.pop('description'))
    else:
        desc = doc.pop('description')
    text.append(('%s\n' % textwrap.fill(CLI.tty_ify(desc), limit, initial_indent=opt_indent, subsequent_indent=opt_indent)))
    if (('deprecated' in doc) and (doc['deprecated'] is not None) and (len(doc['deprecated']) > 0)):
        text.append(('DEPRECATED: \n%s\n' % doc.pop('deprecated')))
    try:
        support_block = self.get_support_block(doc)
        if support_block:
            text.extend(support_block)
    except:
        pass
    if doc.pop('action', False):
        text.append(('  * note: %s\n' % 'This module has a corresponding action plugin.'))
    if (('options' in doc) and doc['options']):
        text.append('OPTIONS (= is mandatory):\n')
        self.add_fields(text, doc.pop('options'), limit, opt_indent)
        text.append('')
    if (('notes' in doc) and doc['notes'] and (len(doc['notes']) > 0)):
        text.append('NOTES:')
        for note in doc['notes']:
            text.append(textwrap.fill(CLI.tty_ify(note), (limit - 6), initial_indent=(opt_indent[:(- 2)] + '* '), subsequent_indent=opt_indent))
        text.append('')
        del doc['notes']
    if (('requirements' in doc) and (doc['requirements'] is not None) and (len(doc['requirements']) > 0)):
        req = ', '.join(doc.pop('requirements'))
        text.append(('REQUIREMENTS:%s\n' % textwrap.fill(CLI.tty_ify(req), (limit - 16), initial_indent='  ', subsequent_indent=opt_indent)))
    for k in sorted(doc):
        if ((k in IGNORE) or (not doc[k])):
            continue
        if isinstance(doc[k], string_types):
            text.append(('%s: %s' % (k.upper(), textwrap.fill(CLI.tty_ify(doc[k]), (limit - (len(k) + 2)), subsequent_indent=opt_indent))))
        elif isinstance(doc[k], (list, tuple)):
            text.append(('%s: %s' % (k.upper(), ', '.join(doc[k]))))
        else:
            text.append(self._dump_yaml({
                k.upper(): doc[k],
            }, opt_indent))
        del doc[k]
    text.append('')
    if (('plainexamples' in doc) and (doc['plainexamples'] is not None)):
        text.append('EXAMPLES:')
        if isinstance(doc['plainexamples'], string_types):
            text.append(doc.pop('plainexamples').strip())
        else:
            text.append(yaml.dump(doc.pop('plainexamples'), indent=2, default_flow_style=False))
        text.append('')
    if (('returndocs' in doc) and (doc['returndocs'] is not None)):
        text.append('RETURN VALUES:\n')
        if isinstance(doc['returndocs'], string_types):
            text.append(doc.pop('returndocs'))
        else:
            text.append(yaml.dump(doc.pop('returndocs'), indent=2, default_flow_style=False))
    text.append('')
    try:
        metadata_block = self.get_metadata_block(doc)
        if metadata_block:
            text.extend(metadata_block)
            text.append('')
    except:
        pass
    return '\n'.join(text)