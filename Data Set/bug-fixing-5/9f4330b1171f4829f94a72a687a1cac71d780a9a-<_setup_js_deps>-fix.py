def _setup_js_deps(self):
    node_version = None
    try:
        node_version = self._run_command(['node', '--version']).rstrip()
    except OSError:
        log.fatal('Cannot find node executable. Please install node and try again.')
        sys.exit(1)
    if (node_version[2] is not None):
        log.info('using node ({0})'.format(node_version))
        self._run_yarn_command(['install', '--production', '--pure-lockfile', '--quiet'])