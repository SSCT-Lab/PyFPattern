def check_for_controlpersist(ssh_executable):
    try:
        return _HAS_CONTROLPERSIST[ssh_executable]
    except KeyError:
        pass
    has_cp = True
    try:
        cmd = subprocess.Popen([ssh_executable, '-o', 'ControlPersist'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = cmd.communicate()
        if ((b'Bad configuration option' in err) or (b'Usage:' in err)):
            has_cp = False
    except OSError:
        has_cp = False
    _HAS_CONTROLPERSIST[ssh_executable] = has_cp
    return has_cp