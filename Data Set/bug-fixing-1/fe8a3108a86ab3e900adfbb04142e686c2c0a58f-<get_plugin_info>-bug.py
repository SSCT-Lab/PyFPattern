

def get_plugin_info(module_dir, limit_to=None, verbose=False):
    "\n    Returns information about plugins and the categories that they belong to\n\n    :arg module_dir: file system path to the top of the plugin directory\n    :kwarg limit_to: If given, this is a list of plugin names to\n        generate information for.  All other plugins will be ignored.\n    :returns: Tuple of two dicts containing module_info, categories, and\n        aliases and a set listing deprecated modules:\n\n        :module_info: mapping of module names to information about them.  The fields of the dict are:\n\n            :path: filesystem path to the module\n            :deprecated: boolean.  True means the module is deprecated otherwise not.\n            :aliases: set of aliases to this module name\n            :metadata: The modules metadata (as recorded in the module)\n            :doc: The documentation structure for the module\n            :seealso: The list of dictionaries with references to related subjects\n            :examples: The module's examples\n            :returndocs: The module's returndocs\n\n        :categories: maps category names to a dict.  The dict contains at\n            least one key, '_modules' which contains a list of module names in\n            that category.  Any other keys in the dict are subcategories with\n            the same structure.\n\n    "
    categories = dict()
    module_info = defaultdict(dict)
    files = (((glob.glob(('%s/*.py' % module_dir)) + glob.glob(('%s/*/*.py' % module_dir))) + glob.glob(('%s/*/*/*.py' % module_dir))) + glob.glob(('%s/*/*/*/*.py' % module_dir)))
    module_index = 0
    for module_path in files:
        if module_path.endswith('__init__.py'):
            continue
        module = os.path.splitext(os.path.basename(module_path))[0]
        if ((module in plugin_docs.BLACKLIST['MODULE']) or (module == 'base')):
            continue
        if ((limit_to is not None) and (module.lower() not in limit_to)):
            continue
        deprecated = False
        if module.startswith('_'):
            if os.path.islink(module_path):
                source = os.path.splitext(os.path.basename(os.path.realpath(module_path)))[0]
                module = module.replace('_', '', 1)
                aliases = module_info[source].get('aliases', set())
                aliases.add(module)
                aliases_deprecated = module_info[source].get('aliases_deprecated', set())
                aliases_deprecated.add(module)
                module_info[source]['aliases'] = aliases
                module_info[source]['aliases_deprecated'] = aliases_deprecated
                continue
            else:
                module = module.replace('_', '', 1)
                deprecated = True
        module_index += 1
        show_progress(module_index)
        (doc, examples, returndocs, metadata) = plugin_docs.get_docstring(module_path, fragment_loader, verbose=verbose)
        if (metadata and ('removed' in metadata.get('status', []))):
            continue
        category = categories
        mod_path_only = os.path.dirname(module_path[len(module_dir):])
        relative_dir = mod_path_only.split('/')[1]
        sub_category = mod_path_only[(len(relative_dir) + 2):]
        primary_category = ''
        module_categories = []
        for new_cat in mod_path_only.split('/')[1:]:
            if (new_cat not in category):
                category[new_cat] = dict()
                category[new_cat]['_modules'] = []
            module_categories.append(new_cat)
            category = category[new_cat]
        category['_modules'].append(module)
        if module_categories:
            primary_category = module_categories[0]
        if (not doc):
            display.error(('*** ERROR: DOCUMENTATION section missing for %s. ***' % module_path))
            continue
        if (('options' in doc) and (doc['options'] is None)):
            display.error('*** ERROR: DOCUMENTATION.options must be a dictionary/hash when used. ***')
            pos = getattr(doc, 'ansible_pos', None)
            if (pos is not None):
                display.error(('Module position: %s, %d, %d' % doc.ansible_pos))
            doc['options'] = dict()
        for (key, opt) in doc.get('options', {
            
        }).items():
            doc['options'][key] = normalize_options(opt)
        module_info[module] = {
            'path': module_path,
            'source': os.path.relpath(module_path, module_dir),
            'deprecated': deprecated,
            'aliases': module_info[module].get('aliases', set()),
            'aliases_deprecated': module_info[module].get('aliases_deprecated', set()),
            'metadata': metadata,
            'doc': doc,
            'examples': examples,
            'returndocs': returndocs,
            'categories': module_categories,
            'primary_category': primary_category,
            'sub_category': sub_category,
        }
    if ('test' in categories):
        del categories['test']
    return (module_info, categories)
