def hostcolor(host, stats, color=True):
    if (ANSIBLE_COLOR and color):
        if ((stats['failures'] != 0) or (stats['unreachable'] != 0)):
            return ('%-37s' % stringc(host, C.COLOR_ERROR))
        elif (stats['changed'] != 0):
            return ('%-37s' % stringc(host, C.COLOR_CHANGED))
        else:
            return ('%-37s' % stringc(host, C.COLOR_OK))
    return ('%-26s' % host)