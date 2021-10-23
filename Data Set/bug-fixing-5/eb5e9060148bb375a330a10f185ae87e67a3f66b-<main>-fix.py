def main():
    p = generate_parser()
    (options, args) = p.parse_args()
    validate_options(options)
    (env, template, outputname) = jinja2_environment(options.template_dir, options.type)
    (mod_info, categories, aliases) = list_modules(options.module_dir)
    categories['all'] = mod_info
    categories['_aliases'] = aliases
    category_names = [c for c in categories.keys() if (not c.startswith('_'))]
    category_names.sort()
    category_list_path = os.path.join(options.output_dir, 'modules_by_category.rst')
    with open(category_list_path, 'wb') as category_list_file:
        category_list_file.write(b'Module Index\n')
        category_list_file.write(b'============\n')
        category_list_file.write(b'\n\n')
        category_list_file.write(b'.. toctree::\n')
        category_list_file.write(b'   :maxdepth: 1\n\n')
        for category in category_names:
            category_list_file.write((b'   list_of_%s_modules\n' % to_bytes(category)))
    module_map = mod_info.copy()
    for modname in module_map:
        result = process_module(modname, options, env, template, outputname, module_map, aliases)
        if (result == 'SKIPPED'):
            del categories['all'][modname]
        else:
            categories['all'][modname] = (categories['all'][modname], result)
    for category in category_names:
        process_category(category, categories, options, env, template, outputname)