def process_category(category, categories, options, env, template, outputname):
    module_map = categories[category]
    module_info = categories['all']
    aliases = {
        
    }
    if ('_aliases' in categories):
        aliases = categories['_aliases']
    category_file_path = os.path.join(options.output_dir, ('list_of_%s_modules.rst' % category))
    category_file = open(category_file_path, 'w')
    print(('*** recording category %s in %s ***' % (category, category_file_path)))
    category = category.replace('_', ' ')
    category = category.title()
    modules = []
    deprecated = []
    for module in module_map.keys():
        if isinstance(module_map[module], dict):
            for mod in (m for m in module_map[module].keys() if (m in module_info)):
                if mod.startswith('_'):
                    deprecated.append(mod)
        else:
            if (module not in module_info):
                continue
            if module.startswith('_'):
                deprecated.append(module)
        modules.append(module)
    modules.sort(key=(lambda k: (k[1:] if k.startswith('_') else k)))
    category_header = ('%s Modules' % category.title())
    underscores = ('`' * len(category_header))
    category_file.write(('%s\n%s\n\n.. toctree:: :maxdepth: 1\n\n' % (category_header, underscores)))
    sections = []
    for module in modules:
        if ((module in module_map) and isinstance(module_map[module], dict)):
            sections.append(module)
            continue
        else:
            print_modules(module, category_file, deprecated, options, env, template, outputname, module_info, aliases)
    sections.sort()
    for section in sections:
        category_file.write(('\n%s\n%s\n\n' % (section.replace('_', ' ').title(), ('-' * len(section)))))
        category_file.write('.. toctree:: :maxdepth: 1\n\n')
        section_modules = module_map[section].keys()
        section_modules.sort(key=(lambda k: (k[1:] if k.startswith('_') else k)))
        for module in (m for m in section_modules if (m in module_info)):
            print_modules(module, category_file, deprecated, options, env, template, outputname, module_info, aliases)
    category_file.write(('\n\n\n.. note::\n    - %s: This marks a module as deprecated, which means a module is kept for backwards compatibility but usage is discouraged.\n       The module documentation details page may explain more about this rationale.\n' % DEPRECATED))
    category_file.close()