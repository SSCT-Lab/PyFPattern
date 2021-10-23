

def main():
    PKG_MANAGERS = get_all_pkg_managers()
    PKG_MANAGER_NAMES = [x.lower() for x in PKG_MANAGERS.keys()]
    global module
    module = AnsibleModule(argument_spec=dict(manager={
        'type': 'list',
        'default': ['auto'],
    }, strategy={
        'choices': ['first', 'all'],
        'default': 'first',
    }), supports_check_mode=True)
    packages = {
        
    }
    results = {
        'ansible_facts': {
            
        },
    }
    managers = [x.lower() for x in module.params['manager']]
    strategy = module.params['strategy']
    if ('auto' in managers):
        managers.extend(PKG_MANAGER_NAMES)
        managers.remove('auto')
    unsupported = set(managers).difference(PKG_MANAGER_NAMES)
    if unsupported:
        if ('auto' in module.params['manager']):
            msg = 'Could not auto detect a usable package manager, check warnings for details.'
        else:
            msg = ('Unsupported package managers requested: %s' % ', '.join(unsupported))
        module.fail_json(msg=msg)
    found = 0
    seen = set()
    for pkgmgr in managers:
        if (found and (strategy == 'first')):
            break
        if (pkgmgr in seen):
            continue
        seen.add(pkgmgr)
        try:
            try:
                manager = PKG_MANAGERS[pkgmgr]()
                if manager.is_available():
                    found += 1
                    packages.update(manager.get_packages())
            except Exception as e:
                if (pkgmgr in module.params['manager']):
                    module.warn(('Requested package manager %s was not usable by this module: %s' % (pkgmgr, to_text(e))))
                continue
            for warning in getattr(manager, 'warnings', []):
                module.warn(warning)
        except Exception as e:
            if (pkgmgr in module.params['manager']):
                module.warn(('Failed to retrieve packages with %s: %s' % (pkgmgr, to_text(e))))
    if (found == 0):
        msg = ('Could not detect a supported package manager from the following list: %s, or the required Python library is not installed. Check warnings for details.' % managers)
        module.fail_json(msg=msg)
    results['ansible_facts']['packages'] = packages
    module.exit_json(**results)
