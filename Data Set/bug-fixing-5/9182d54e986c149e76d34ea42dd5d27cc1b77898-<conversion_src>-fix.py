def conversion_src(module):
    src_list = module.params['src'].split('\n')
    src_list_organize = []
    if (src_list[0].strip() == '#'):
        src_list.pop(0)
    for per_config in src_list:
        if (per_config.strip() == '#'):
            src_list_organize.append('quit')
        else:
            src_list_organize.append(per_config)
    src_str = '\n'.join(src_list_organize)
    return src_str