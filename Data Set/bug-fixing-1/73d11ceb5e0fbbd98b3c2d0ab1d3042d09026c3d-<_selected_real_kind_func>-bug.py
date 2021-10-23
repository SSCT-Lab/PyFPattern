

def _selected_real_kind_func(p, r=0, radix=0):
    if (p < 7):
        return 4
    if (p < 16):
        return 8
    machine = platform.machine().lower()
    if (machine.startswith('power') or machine.startswith('ppc64')):
        if (p <= 20):
            return 16
    elif (p < 19):
        return 10
    elif (p <= 20):
        return 16
    return (- 1)
