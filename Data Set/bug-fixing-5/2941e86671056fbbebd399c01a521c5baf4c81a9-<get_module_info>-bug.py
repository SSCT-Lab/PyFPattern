def get_module_info(module_dir, limit_to_modules=None, verbose=False):
    "\n    Returns information about modules and the categories that they belong to\n\n    :arg module_dir: file system path to the top of the modules directory\n    :kwarg limit_to_modules: If given, this is a list of module names to\n        generate information for.  All other modules will be ignored.\n    :returns: Tuple of two dicts containing module_info, categories, and\n        aliases and a set listing deprecated modules:\n\n        :module_info: mapping of module names to information about them.  The fields of the dict are:\n\n            :path: filesystem path to the module\n            :deprecated: boolean.  True means the module is deprecated otherwise not.\n            :aliases: set of aliases to this module name\n            :metadata: The modules metadata (as recorded in the module)\n            :doc: The documentation structure for the module\n            :examples: The module's examples\n            :returndocs: The module's returndocs\n\n        :categories: maps category names to a dict.  The dict contains at\n            least one key, '_modules' which contains a list of module names in\n            that category.  Any other keys in the dict are subcategories with\n            the same structure.\n    "
    categories = dict()
    module_info = defaultdict(dict)
    files = (((glob.glob(('%s/*.py' % module_dir)) + glob.glob(('%s/*/*.py' % module_dir))) + glob.glob(('%s/*/*/*.py' % module_dir))) + glob.glob(('%s/*/*/*/*.py' % module_dir)))
    for module_path in files:
        if module_path.endswith('__init__.py'):
            continue
        module = os.path.splitext(os.path.basename(module_path))[0]
        if (module in plugin_docs.BLACKLIST['MODULE']):
            continue
        if ((limit_to_modules is not None) and (module.lower() in limit_to_modules)):
            continue
        deprecated = False
        if module.startswith('_'):
            if os.path.islink(module_path):
                source = os.path.splitext(os.path.basename(os.path.realpath(module_path)))[0]
                module = module.replace('_', '', 1)
                aliases = module_info[source].get('aliases', set())
                aliases.add(module)
                module_info[source]['aliases'] = aliases
                continue
            else:
                module = module.replace('_', '', 1)
                deprecated = True
        category = categories
        mod_path_only = os.path.dirname(module_path[len(module_dir):])
        for new_cat in mod_path_only.split('/')[1:]:
            if (new_cat not in category):
                category[new_cat] = dict()
                category[new_cat]['_modules'] = []
            category = category[new_cat]
        category['_modules'].append(module)
        (doc, examples, returndocs, metadata) = plugin_docs.get_docstring(module_path, verbose=verbose)
        module_info[module] = {
            'path': module_path,
            'deprecated': deprecated,
            'aliases': set(),
            'metadata': metadata,
            'doc': doc,
            'examples': examples,
            'returndocs': returndocs,
        }
    if ('test' in categories):
        del categories['test']
    return (module_info, categories)