def create_apache_identifier(name):
    "\n    By convention if a module is loaded via name, it appears in apache2ctl -M as\n    name_module.\n\n    Some modules don't follow this convention and we use replacements for those."
    text_workarounds = [('shib2', 'mod_shib'), ('evasive', 'evasive20_module')]
    re_workarounds = [('php', '^(php\\d)\\.')]
    for (a2enmod_spelling, module_name) in text_workarounds:
        if (a2enmod_spelling in name):
            return module_name
    for (search, reexpr) in re_workarounds:
        if (search in name):
            rematch = re.search(reexpr, name)
            return (rematch.group(1) + '_module')
    return (name + '_module')