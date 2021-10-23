def parse_zypper_xml(m, cmd, fail_not_found=True, packages=None):
    (rc, stdout, stderr) = m.run_command(cmd, check_rc=False)
    try:
        dom = parseXML(stdout)
    except xml.parsers.expat.ExpatError as exc:
        m.fail_json(msg=('Failed to parse zypper xml output: %s' % to_native(exc)), rc=rc, stdout=stdout, stderr=stderr, cmd=cmd)
    if (rc == 104):
        if fail_not_found:
            errmsg = dom.getElementsByTagName('message')[(- 1)].childNodes[0].data
            m.fail_json(msg=errmsg, rc=rc, stdout=stdout, stderr=stderr, cmd=cmd)
        else:
            return ({
                
            }, rc, stdout, stderr)
    elif (rc in [0, 106, 103]):
        if (packages is None):
            firstrun = True
            packages = {
                
            }
        solvable_list = dom.getElementsByTagName('solvable')
        for solvable in solvable_list:
            name = solvable.getAttribute('name')
            packages[name] = {
                
            }
            packages[name]['version'] = solvable.getAttribute('edition')
            packages[name]['oldversion'] = solvable.getAttribute('edition-old')
            status = solvable.getAttribute('status')
            packages[name]['installed'] = (status == 'installed')
            packages[name]['group'] = solvable.parentNode.nodeName
        if ((rc == 103) and firstrun):
            return parse_zypper_xml(m, cmd, fail_not_found=fail_not_found, packages=packages)
        return (packages, rc, stdout, stderr)
    m.fail_json(msg=('Zypper run command failed with return code %s.' % rc), rc=rc, stdout=stdout, stderr=stderr, cmd=cmd)