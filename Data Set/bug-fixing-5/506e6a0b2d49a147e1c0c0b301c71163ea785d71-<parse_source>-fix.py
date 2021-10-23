def parse_source(self, source, cache=False):
    ' Generate or update inventory for the source provided '
    parsed = False
    display.debug(('Examining possible inventory source: %s' % source))
    b_source = to_bytes(source)
    if os.path.isdir(b_source):
        display.debug(('Searching for inventory files in directory: %s' % source))
        for i in sorted(os.listdir(b_source)):
            display.debug(('Considering %s' % i))
            if IGNORED.search(i):
                continue
            fullpath = os.path.join(b_source, i)
            parsed_this_one = self.parse_source(to_native(fullpath))
            display.debug(('parsed %s as %s' % (fullpath, parsed_this_one)))
            if (not parsed):
                parsed = parsed_this_one
    else:
        self._inventory.current_source = source
        if (not self._inventory_plugins):
            self._setup_inventory_plugins()
        failures = []
        for plugin in self._inventory_plugins:
            plugin_name = to_native(getattr(plugin, '_load_name', getattr(plugin, '_original_path', '')))
            display.debug(('Attempting to use plugin %s (%s)' % (plugin_name, plugin._original_path)))
            if plugin.verify_file(source):
                try:
                    plugin.parse(self._inventory, self._loader, source, cache=cache)
                    parsed = True
                    display.vvv(('Parsed %s inventory source with %s plugin' % (to_native(source), plugin_name)))
                    break
                except AnsibleParserError as e:
                    display.debug(('%s did not meet %s requirements' % (to_native(source), plugin_name)))
                    failures.append({
                        'src': source,
                        'plugin': plugin_name,
                        'exc': e,
                    })
            else:
                display.debug(('%s did not meet %s requirements' % (to_native(source), plugin_name)))
        else:
            if ((not parsed) and failures):
                if C.INVENTORY_UNPARSED_IS_FAILED:
                    msg = ('Could not parse inventory source %s with available plugins:\n' % source)
                    for fail in failures:
                        msg += ('Plugin %s failed: %s\n' % (fail['plugin'], to_native(fail['exc'])))
                        if (display.verbosity >= 3):
                            msg += ('%s\n' % fail['exc'].tb)
                    raise AnsibleParserError(msg)
                else:
                    for fail in failures:
                        display.warning(('\n* Failed to parse %s with %s plugin: %s' % (to_native(fail['src']), fail['plugin'], to_native(fail['exc']))))
                        display.vvv(fail['exc'].tb)
    if (not parsed):
        display.warning(('Unable to parse %s as an inventory source' % to_native(source)))
    self._inventory.current_source = None
    return parsed