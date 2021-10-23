

def get_api_init_text(package, api_name):
    'Get a map from destination module to __init__.py code for that module.\n\n  Args:\n    package: Base python package containing python with target tf_export\n      decorators.\n    api_name: API you want to generate (e.g. `tensorflow` or `estimator`).\n\n  Returns:\n    A dictionary where\n      key: (string) destination module (for e.g. tf or tf.consts).\n      value: (string) text that should be in __init__.py files for\n        corresponding modules.\n  '
    module_code_builder = _ModuleInitCodeBuilder()
    for module in list(sys.modules.values()):
        if ((not module) or (not hasattr(module, '__name__')) or (module.__name__ is None) or (package not in module.__name__)):
            continue
        if (('.contrib.' in module.__name__) or module.__name__.endswith('.contrib')):
            continue
        for module_contents_name in dir(module):
            if (((module.__name__ + '.') + module_contents_name) in _SYMBOLS_TO_SKIP_EXPLICITLY):
                continue
            attr = getattr(module, module_contents_name)
            if (module_contents_name == API_ATTRS[api_name].constants):
                for (exports, value) in attr:
                    for export in exports:
                        names = export.split('.')
                        dest_module = '.'.join(names[:(- 1)])
                        module_code_builder.add_import((- 1), dest_module, module.__name__, value, names[(- 1)])
                continue
            (_, attr) = tf_decorator.unwrap(attr)
            if (hasattr(attr, '__dict__') and (API_ATTRS[api_name].names in attr.__dict__)):
                for export in getattr(attr, API_ATTRS[api_name].names):
                    names = export.split('.')
                    dest_module = '.'.join(names[:(- 1)])
                    module_code_builder.add_import(id(attr), dest_module, module.__name__, module_contents_name, names[(- 1)])
    imported_modules = set(module_code_builder.module_imports.keys())
    import_from = '.'
    for module in imported_modules:
        if (not module):
            continue
        module_split = module.split('.')
        parent_module = ''
        for submodule_index in range(len(module_split)):
            if (submodule_index > 0):
                parent_module += (('.' + module_split[(submodule_index - 1)]) if parent_module else module_split[(submodule_index - 1)])
            module_code_builder.add_import((- 1), parent_module, import_from, module_split[submodule_index], module_split[submodule_index])
    return module_code_builder.build()
