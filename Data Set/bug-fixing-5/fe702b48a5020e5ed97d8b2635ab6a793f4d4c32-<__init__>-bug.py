def __init__(self, play_context, new_stdin, *args, **kwargs):
    super(Connection, self).__init__(play_context, new_stdin, *args, **kwargs)
    self._ssh_shell = None
    self._matched_prompt = None
    self._matched_pattern = None
    self._last_response = None
    self._history = list()
    self._local = connection_loader.get('local', play_context, '/dev/null')
    self._local.set_options()
    self._terminal = None
    self._cliconf = None
    if (self._play_context.verbosity > 3):
        logging.getLogger('paramiko').setLevel(logging.DEBUG)
    self._update_connection_state()