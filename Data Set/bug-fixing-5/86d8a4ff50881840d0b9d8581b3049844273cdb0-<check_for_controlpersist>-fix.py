def check_for_controlpersist(ssh_executable):
    try:
        return _HAS_CONTROLPERSIST[ssh_executable]
    except KeyError:
        pass
    b_ssh_exec = to_bytes(ssh_executable, errors='surrogate_or_strict')
    has_cp = True
    try:
        cmd = subprocess.Popen([b_ssh_exec, '-o', 'ControlPersist'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = cmd.communicate()
        if ((b'Bad configuration option' in err) or (b'Usage:' in err)):
            has_cp = False
    except OSError:
        has_cp = False
    _HAS_CONTROLPERSIST[ssh_executable] = has_cp
    return has_cp