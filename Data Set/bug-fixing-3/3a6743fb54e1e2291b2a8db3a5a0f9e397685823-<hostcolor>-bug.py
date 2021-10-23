def hostcolor(host, stats, color=True):
    if (ANSIBLE_COLOR and color):
        if ((stats['failures'] != 0) or (stats['unreachable'] != 0)):
            return ('%-37s' % stringc(host, 'red'))
        elif (stats['changed'] != 0):
            return ('%-37s' % stringc(host, 'yellow'))
        else:
            return ('%-37s' % stringc(host, 'green'))
    return ('%-26s' % host)