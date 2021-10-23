def build_ping(dest, count=None, source=None, vrf=None):
    "\n    Function to build the command to send to the terminal for the switch\n    to execute. All args come from the module's unique params.\n    "
    if (vrf is not None):
        cmd = 'ping {0} {1}'.format(vrf, dest)
    else:
        cmd = 'ping {0}'.format(dest)
    if (count is not None):
        cmd += ' repeat {0}'.format(str(count))
    if (source is not None):
        cmd += ' source {0}'.format(source)
    return cmd