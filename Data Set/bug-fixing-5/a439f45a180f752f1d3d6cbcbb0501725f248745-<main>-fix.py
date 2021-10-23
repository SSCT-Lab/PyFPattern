def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True, type='list'), state=dict(required=True, choices=['absent', 'installed', 'latest', 'present', 'removed']), build=dict(default='no', type='bool'), ports_dir=dict(default='/usr/ports'), quick=dict(default='no', type='bool'), clean=dict(default='no', type='bool')), supports_check_mode=True)
    name = module.params['name']
    state = module.params['state']
    build = module.params['build']
    ports_dir = module.params['ports_dir']
    rc = 0
    stdout = ''
    stderr = ''
    result = {
        
    }
    result['name'] = name
    result['state'] = state
    result['build'] = build
    pkg_spec = {
        
    }
    if (build is True):
        if (not os.path.isdir(ports_dir)):
            module.fail_json(msg=('the ports source directory %s does not exist' % ports_dir))
        parse_package_name(['sqlports'], pkg_spec, module)
        get_package_state(['sqlports'], pkg_spec, module)
        if (not pkg_spec['sqlports']['installed_state']):
            module.debug(("main(): installing 'sqlports' because build=%s" % module.params['build']))
            package_present(['sqlports'], pkg_spec, module)
    asterisk_name = False
    for n in name:
        if (n == '*'):
            if (len(name) != 1):
                module.fail_json(msg="the package name '*' can not be mixed with other names")
            asterisk_name = True
    if asterisk_name:
        if (state != 'latest'):
            module.fail_json(msg="the package name '*' is only valid when using state=latest")
        else:
            upgrade_packages(pkg_spec, module)
    else:
        parse_package_name(name, pkg_spec, module)
        for n in name:
            if (pkg_spec[n]['branch'] and (module.params['build'] is True)):
                module.fail_json(msg=("the combination of 'branch' syntax and build=%s is not supported: %s" % (module.params['build'], n)))
        get_package_state(name, pkg_spec, module)
        if (state in ['installed', 'present']):
            package_present(name, pkg_spec, module)
        elif (state in ['absent', 'removed']):
            package_absent(name, pkg_spec, module)
        elif (state == 'latest'):
            package_latest(name, pkg_spec, module)
    combined_changed = False
    combined_error_message = ''
    for n in name:
        if (pkg_spec[n]['rc'] != 0):
            if pkg_spec[n]['stderr']:
                if combined_error_message:
                    combined_error_message += (', %s' % pkg_spec[n]['stderr'])
                else:
                    combined_error_message = pkg_spec[n]['stderr']
            elif combined_error_message:
                combined_error_message += (', %s' % pkg_spec[n]['stdout'])
            else:
                combined_error_message = pkg_spec[n]['stdout']
        if (pkg_spec[n]['changed'] is True):
            combined_changed = True
    if combined_error_message:
        module.fail_json(msg=combined_error_message)
    result['changed'] = combined_changed
    module.exit_json(**result)