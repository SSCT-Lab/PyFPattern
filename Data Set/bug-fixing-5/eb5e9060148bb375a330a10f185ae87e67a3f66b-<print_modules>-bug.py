def print_modules(module, category_file, deprecated, options, env, template, outputname, module_map, aliases):
    modstring = module
    if modstring.startswith('_'):
        modstring = module[1:]
    modname = modstring
    if (module in deprecated):
        modstring = (modstring + DEPRECATED)
    category_file.write(('  %s - %s <%s_module>\n' % (to_bytes(modstring), to_bytes(rst_ify(module_map[module][1])), to_bytes(modname))))