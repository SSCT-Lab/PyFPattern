def jinja2_environment(template_dir, typ, plugin_type):
    env = Environment(loader=FileSystemLoader(template_dir), variable_start_string='@{', variable_end_string='}@', trim_blocks=True)
    env.globals['xline'] = rst_xline
    env.globals['to_kludge_ns'] = to_kludge_ns
    env.globals['from_kludge_ns'] = from_kludge_ns
    if ('max' not in env.filters):
        env.filters['max'] = do_max
    templates = {
        
    }
    if (typ == 'rst'):
        env.filters['rst_ify'] = rst_ify
        env.filters['html_ify'] = html_ify
        env.filters['fmt'] = rst_fmt
        env.filters['xline'] = rst_xline
        env.filters['documented_type'] = documented_type
        env.tests['list'] = test_list
        templates['plugin'] = env.get_template('plugin.rst.j2')
        templates['plugin_deprecation_stub'] = env.get_template('plugin_deprecation_stub.rst.j2')
        if (plugin_type == 'module'):
            name = 'modules'
        else:
            name = 'plugins'
        templates['category_list'] = env.get_template(('%s_by_category.rst.j2' % name))
        templates['support_list'] = env.get_template(('%s_by_support.rst.j2' % name))
        templates['list_of_CATEGORY_modules'] = env.get_template(('list_of_CATEGORY_%s.rst.j2' % name))
    else:
        raise Exception(('Unsupported format type: %s' % typ))
    return templates