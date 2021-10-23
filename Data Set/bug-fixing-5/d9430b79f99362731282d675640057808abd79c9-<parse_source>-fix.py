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
            b_fullpath = os.path.join(b_source, i)
            parsed_this_one = self.parse_source(b_fullpath, cache=cache)
            display.debug(('parsed %s as %s' % (to_text(b_fullpath), parsed_this_one)))
            if (not parsed):
                parsed = parsed_this_one
    else:
        self._inventory.current_source = source
        if (not self._inventory_plugins):
            self._setup_inventory_plugins()
        failures = []
        for plugin in self._inventory_plugins:
            plugin_name = to_text(getattr(plugin, '_load_name', getattr(plugin, '_original_path', '')))
            display.debug(('Attempting to use plugin %s (%s)' % (plugin_name, plugin._original_path)))
            try:
                plugin_wants = bool(plugin.verify_file(source))
            except Exception:
                plugin_wants = False
            if plugin_wants:
                try:
                    plugin.parse(self._inventory, self._loader, source, cache=cache)
                    parsed = True
                    display.vvv(('Parsed %s inventory source with %s plugin' % (to_text(source), plugin_name)))
                    break
                except AnsibleParserError as e:
                    display.debug(('%s was not parsable by %s' % (to_text(source), plugin_name)))
                    failures.append({
                        'src': source,
                        'plugin': plugin_name,
                        'exc': e,
                    })
                except Exception as e:
                    display.debug(('%s failed to parse %s' % (plugin_name, to_text(source))))
                    failures.append({
                        'src': source,
                        'plugin': plugin_name,
                        'exc': AnsibleError(e),
                    })
            else:
                display.debug(('%s did not meet %s requirements' % (to_text(source), plugin_name)))
        else:
            if ((not parsed) and failures):
                for fail in failures:
                    display.warning(('\n* Failed to parse %s with %s plugin: %s' % (to_text(fail['src']), fail['plugin'], to_text(fail['exc']))))
                    if hasattr(fail['exc'], 'tb'):
                        display.vvv(to_text(fail['exc'].tb))
    if (not parsed):
        display.warning(('Unable to parse %s as an inventory source' % to_text(source)))
    self._inventory.current_source = None
    return parsed