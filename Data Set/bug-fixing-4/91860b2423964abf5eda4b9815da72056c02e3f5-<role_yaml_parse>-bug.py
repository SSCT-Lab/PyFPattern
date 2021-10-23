@staticmethod
def role_yaml_parse(role):
    if isinstance(role, string_types):
        name = None
        scm = None
        src = None
        version = None
        if (',' in role):
            if (role.count(',') == 1):
                (src, version) = role.strip().split(',', 1)
            elif (role.count(',') == 2):
                (src, version, name) = role.strip().split(',', 2)
            else:
                raise AnsibleError(("Invalid role line (%s). Proper format is 'role_name[,version[,name]]'" % role))
        else:
            src = role
        if (name is None):
            name = RoleRequirement.repo_url_to_role_name(src)
        if ('+' in src):
            (scm, src) = src.split('+', 1)
        return dict(name=name, src=src, scm=scm, version=version)
    if ('role' in role):
        role = RoleRequirement.role_spec_parse(role['role'])
    else:
        role = role.copy()
        if ('src' in role):
            if (('github.com' in role['src']) and ('http' in role['src']) and ('+' not in role['src']) and (not role['src'].endswith('.tar.gz'))):
                role['src'] = ('git+' + role['src'])
            if ('+' in role['src']):
                (scm, src) = role['src'].split('+')
                role['scm'] = scm
                role['src'] = src
            if ('name' not in role):
                role['name'] = RoleRequirement.repo_url_to_role_name(role['src'])
        if ('version' not in role):
            role['version'] = ''
        if ('scm' not in role):
            role['scm'] = None
    for key in list(role.keys()):
        if (key not in VALID_SPEC_KEYS):
            role.pop(key)
    return role