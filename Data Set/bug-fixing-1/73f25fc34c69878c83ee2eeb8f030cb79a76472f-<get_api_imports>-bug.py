

def get_api_imports():
    "Get a map from destination module to formatted imports.\n\n  Returns:\n    A dictionary where\n      key: (string) destination module (for e.g. tf or tf.consts).\n      value: List of strings representing module imports\n          (for e.g. 'from foo import bar') and constant\n          assignments (for e.g. 'FOO = 123').\n  "
    module_imports_builder = _ModuleImportsBuilder()
    visited_symbols = set()
    for module in sys.modules.values():
        if ((not module) or ('tensorflow.' not in module.__name__)):
            continue
        if (('.contrib.' in module.__name__) or module.__name__.endswith('.contrib')):
            continue
        for module_contents_name in dir(module):
            attr = getattr(module, module_contents_name)
            if (id(attr) in visited_symbols):
                continue
            if (module_contents_name == _API_CONSTANTS_ATTR):
                for (exports, value) in attr:
                    for export in exports:
                        names = export.split('.')
                        dest_module = '.'.join(names[:(- 1)])
                        module_imports_builder.add_import(dest_module, module.__name__, value, names[(- 1)])
                continue
            (_, attr) = tf_decorator.unwrap(attr)
            if (hasattr(attr, '__dict__') and (_API_NAMES_ATTR in attr.__dict__)):
                if (id(attr) in visited_symbols):
                    continue
                visited_symbols.add(id(attr))
                for export in attr._tf_api_names:
                    names = export.split('.')
                    dest_module = '.'.join(names[:(- 1)])
                    module_imports_builder.add_import(dest_module, module.__name__, module_contents_name, names[(- 1)])
    imported_modules = set(module_imports_builder.module_imports.keys())
    for module in imported_modules:
        if (not module):
            continue
        module_split = module.split('.')
        parent_module = ''
        for submodule_index in range(len(module_split)):
            import_from = _OUTPUT_MODULE
            if (submodule_index > 0):
                parent_module += (('.' + module_split[(submodule_index - 1)]) if parent_module else module_split[(submodule_index - 1)])
                import_from += ('.' + parent_module)
            module_imports_builder.add_import(parent_module, import_from, module_split[submodule_index], module_split[submodule_index])
    return module_imports_builder.module_imports
