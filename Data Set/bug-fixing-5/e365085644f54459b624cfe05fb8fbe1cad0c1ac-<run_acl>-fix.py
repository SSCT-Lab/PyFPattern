def run_acl(module, cmd, check_rc=True):
    try:
        (rc, out, err) = module.run_command(' '.join(cmd), check_rc=check_rc)
    except Exception:
        e = get_exception()
        module.fail_json(msg=e.strerror)
    lines = []
    for l in out.splitlines():
        if (not l.startswith('#')):
            lines.append(l.strip())
    if (lines and (not lines[(- 1)].split())):
        return lines[:(- 1)]
    return lines