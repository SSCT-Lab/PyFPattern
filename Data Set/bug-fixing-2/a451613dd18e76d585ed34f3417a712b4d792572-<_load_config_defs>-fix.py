

def _load_config_defs(self, name, path):
    ' Reads plugin docs to find configuration setting definitions, to push to config manager for later use '
    if self.class_name:
        type_name = get_plugin_class(self.class_name)
        if (type_name in ('callback', 'connection', 'inventory', 'lookup', 'shell')):
            dstring = get_docstring(path, fragment_loader, verbose=False, ignore_errors=True)[0]
            if (dstring and ('options' in dstring) and isinstance(dstring['options'], dict)):
                C.config.initialize_plugin_configuration_definitions(type_name, name, dstring['options'])
                display.debug(('Loaded config def from plugin (%s/%s)' % (type_name, name)))
