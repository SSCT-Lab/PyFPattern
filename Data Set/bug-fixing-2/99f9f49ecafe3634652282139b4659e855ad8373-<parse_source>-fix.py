

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
            fullpath = to_text(os.path.join(b_source, i), errors='surrogate_or_strict')
            parsed_this_one = self.parse_source(fullpath, cache=cache)
            display.debug(('parsed %s as %s' % (fullpath, parsed_this_one)))
            if (not parsed):
                parsed = parsed_this_one
    else:
        self._inventory.current_source = source
        failures = []
        for plugin in self._fetch_inventory_plugins():
            plugin_name = to_text(getattr(plugin, '_load_name', getattr(plugin, '_original_path', '')))
            display.debug(('Attempting to use plugin %s (%s)' % (plugin_name, plugin._original_path)))
            try:
                plugin_wants = bool(plugin.verify_file(source))
            except Exception:
                plugin_wants = False
            if plugin_wants:
                try:
                    plugin.parse(self._inventory, self._loader, source, cache=cache)
                    try:
                        plugin.update_cache_if_changed()
                    except AttributeError:
                        pass
                    parsed = True
                    display.vvv(('Parsed %s inventory source with %s plugin' % (source, plugin_name)))
                    break
                except AnsibleParserError as e:
                    display.debug(('%s was not parsable by %s' % (source, plugin_name)))
                    tb = ''.join(traceback.format_tb(sys.exc_info()[2]))
                    failures.append({
                        'src': source,
                        'plugin': plugin_name,
                        'exc': e,
                        'tb': tb,
                    })
                except Exception as e:
                    display.debug(('%s failed while attempting to parse %s' % (plugin_name, source)))
                    tb = ''.join(traceback.format_tb(sys.exc_info()[2]))
                    failures.append({
                        'src': source,
                        'plugin': plugin_name,
                        'exc': AnsibleError(e),
                        'tb': tb,
                    })
            else:
                display.vvv(('%s declined parsing %s as it did not pass its verify_file() method' % (plugin_name, source)))
        else:
            if ((not parsed) and failures):
                for fail in failures:
                    display.warning(('\n* Failed to parse %s with %s plugin: %s' % (to_text(fail['src']), fail['plugin'], to_text(fail['exc']))))
                    if ('tb' in fail):
                        display.vvv(to_text(fail['tb']))
                if C.INVENTORY_ANY_UNPARSED_IS_FAILED:
                    raise AnsibleError(('Completely failed to parse inventory source %s' % source))
    if (not parsed):
        if ((source != '/etc/ansible/hosts') or os.path.exists(source)):
            display.warning(('Unable to parse %s as an inventory source' % source))
    self._inventory.current_source = None
    return parsed
