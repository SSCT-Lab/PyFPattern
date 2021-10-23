def get_plugin_list_text(self, loader):
    columns = display.columns
    displace = max((len(x) for x in self.plugin_list))
    linelimit = ((columns - displace) - 5)
    text = []
    deprecated = []
    for plugin in sorted(self.plugin_list):
        try:
            filename = loader.find_plugin(plugin, mod_type='.py', ignore_deprecated=True, check_aliases=True)
            if (filename is None):
                continue
            if filename.endswith('.ps1'):
                continue
            if os.path.isdir(filename):
                continue
            doc = None
            try:
                (doc, plainexamples, returndocs, metadata) = get_docstring(filename, fragment_loader)
            except:
                display.warning(('%s has a documentation formatting error' % plugin))
            if ((not doc) or (not isinstance(doc, dict))):
                desc = 'UNDOCUMENTED'
                display.warning(('%s parsing did not produce documentation.' % plugin))
            else:
                desc = self.tty_ify(doc.get('short_description', 'INVALID SHORT DESCRIPTION').strip())
            if (len(desc) > linelimit):
                desc = (desc[:linelimit] + '...')
            if plugin.startswith('_'):
                deprecated.append(('%-*s %-*.*s' % (displace, plugin[1:], linelimit, len(desc), desc)))
            else:
                text.append(('%-*s %-*.*s' % (displace, plugin, linelimit, len(desc), desc)))
        except Exception as e:
            raise AnsibleError(('Failed reading docs at %s: %s' % (plugin, to_native(e))))
    if (len(deprecated) > 0):
        text.append('\nDEPRECATED:')
        text.extend(deprecated)
    return '\n'.join(text)