def repolist(module, repoq, qf='%{repoid}'):
    cmd = (repoq + ['--qf', qf, '-a'])
    (rc, out, err) = module.run_command(cmd)
    ret = []
    if (rc == 0):
        ret = set([p for p in out.split('\n') if p.strip()])
    return ret