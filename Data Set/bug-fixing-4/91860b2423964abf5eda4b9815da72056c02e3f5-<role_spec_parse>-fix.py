@staticmethod
def role_spec_parse(role_spec):
    display.deprecated(('The comma separated role spec format, use the yaml/explicit format instead. Line that trigger this: %s' % role_spec))
    default_role_versions = dict(git='master', hg='tip')
    role_spec = role_spec.strip()
    role_version = ''
    if ((role_spec == '') or role_spec.startswith('#')):
        return (None, None, None, None)
    tokens = [s.strip() for s in role_spec.split(',')]
    if (('github.com/' in tokens[0]) and (not tokens[0].startswith('git+')) and (not tokens[0].endswith('.tar.gz'))):
        tokens[0] = ('git+' + tokens[0])
    if ('+' in tokens[0]):
        (scm, role_url) = tokens[0].split('+')
    else:
        scm = None
        role_url = tokens[0]
    if (len(tokens) >= 2):
        role_version = tokens[1]
    if (len(tokens) == 3):
        role_name = tokens[2]
    else:
        role_name = RoleRequirement.repo_url_to_role_name(tokens[0])
    if (scm and (not role_version)):
        role_version = default_role_versions.get(scm, '')
    return dict(scm=scm, src=role_url, version=role_version, name=role_name)