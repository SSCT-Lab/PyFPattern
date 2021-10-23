def execute_install(self):
    '\n        Executes the installation action. The args list contains the\n        roles to be installed, unless -f was specified. The list of roles\n        can be a name (which will be downloaded via the galaxy API and github),\n        or it can be a local .tar.gz file.\n        '
    role_file = self.get_opt('role_file', None)
    if ((len(self.args) == 0) and (role_file is None)):
        raise AnsibleOptionsError('- you must specify a user/role name or a roles file')
    elif ((len(self.args) == 1) and (role_file is not None)):
        raise AnsibleOptionsError('- please specify a user/role name, or a roles file, but not both')
    no_deps = self.get_opt('no_deps', False)
    force = self.get_opt('force', False)
    roles_left = []
    if role_file:
        try:
            f = open(role_file, 'r')
            if (role_file.endswith('.yaml') or role_file.endswith('.yml')):
                try:
                    required_roles = yaml.safe_load(f.read())
                except Exception as e:
                    raise AnsibleError(('Unable to load data from the requirements file: %s' % role_file))
                if (required_roles is None):
                    raise AnsibleError(('No roles found in file: %s' % role_file))
                for role in required_roles:
                    if ('include' not in role):
                        role = RoleRequirement.role_yaml_parse(role)
                        display.vvv(('found role %s in yaml file' % str(role)))
                        if (('name' not in role) and ('scm' not in role)):
                            raise AnsibleError('Must specify name or src for role')
                        roles_left.append(GalaxyRole(self.galaxy, **role))
                    else:
                        with open(role['include']) as f_include:
                            try:
                                roles_left += [GalaxyRole(self.galaxy, **r) for r in map(RoleRequirement.role_yaml_parse, yaml.safe_load(f_include))]
                            except Exception as e:
                                msg = 'Unable to load data from the include requirements file: %s %s'
                                raise AnsibleError((msg % (role_file, e)))
            else:
                display.deprecated('going forward only the yaml format will be supported')
                for rline in f.readlines():
                    if (rline.startswith('#') or (rline.strip() == '')):
                        continue
                    display.debug(('found role %s in text file' % str(rline)))
                    role = RoleRequirement.role_yaml_parse(rline.strip())
                    roles_left.append(GalaxyRole(self.galaxy, **role))
            f.close()
        except (IOError, OSError) as e:
            display.error(('Unable to open %s: %s' % (role_file, str(e))))
    else:
        for rname in self.args:
            role = RoleRequirement.role_yaml_parse(rname.strip())
            roles_left.append(GalaxyRole(self.galaxy, **role))
    for role in roles_left:
        display.vvv(('Installing role %s ' % role.name))
        if (role.install_info is not None):
            if (role.install_info['version'] != role.version):
                if force:
                    display.display(('- changing role %s from %s to %s' % (role.name, role.install_info['version'], (role.version or 'unspecified'))))
                    role.remove()
                else:
                    display.warning(('- %s (%s) is already installed - use --force to change version to %s' % (role.name, role.install_info['version'], (role.version or 'unspecified'))))
                    continue
            else:
                display.display(('- %s is already installed, skipping.' % str(role)))
                continue
        try:
            installed = role.install()
        except AnsibleError as e:
            display.warning(('- %s was NOT installed successfully: %s ' % (role.name, str(e))))
            self.exit_without_ignore()
            continue
        if ((not no_deps) and installed):
            role_dependencies = (role.metadata.get('dependencies') or [])
            for dep in role_dependencies:
                display.debug(('Installing dep %s' % dep))
                dep_req = RoleRequirement()
                dep_info = dep_req.role_yaml_parse(dep)
                dep_role = GalaxyRole(self.galaxy, **dep_info)
                if (('.' not in dep_role.name) and ('.' not in dep_role.src) and (dep_role.scm is None)):
                    continue
                if (dep_role.install_info is None):
                    if (dep_role not in roles_left):
                        display.display(('- adding dependency: %s' % str(dep_role)))
                        roles_left.append(dep_role)
                    else:
                        display.display(('- dependency %s already pending installation.' % dep_role.name))
                elif (dep_role.install_info['version'] != dep_role.version):
                    display.warning(('- dependency %s from role %s differs from already installed version (%s), skipping' % (str(dep_role), role.name, dep_role.install_info['version'])))
                else:
                    display.display(('- dependency %s is already installed, skipping.' % dep_role.name))
        if (not installed):
            display.warning(('- %s was NOT installed successfully.' % role.name))
            self.exit_without_ignore()
    return 0