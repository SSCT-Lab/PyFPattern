def list_items(module, base, command):
    'List package info based on the command.'
    if (command == 'updates'):
        command = 'upgrades'
    if (command in ['installed', 'upgrades', 'available']):
        results = [_package_dict(package) for package in getattr(base.sack.query(), command)()]
    elif (command in ['repos', 'repositories']):
        results = [{
            'repoid': repo.id,
            'state': 'enabled',
        } for repo in base.repos.iter_enabled()]
    else:
        packages = dnf.subject.Subject(command).get_best_query(base.sack)
        results = [_package_dict(package) for package in packages]
    base.close()
    module.exit_json(results=results)