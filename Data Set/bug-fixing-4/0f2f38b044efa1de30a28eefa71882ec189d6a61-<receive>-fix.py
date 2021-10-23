def receive(self, command=None, prompts=None, answer=None, newline=True, prompt_retry_check=False, check_all=False):
    '\n        Handles receiving of output from command\n        '
    self._matched_prompt = None
    self._matched_cmd_prompt = None
    recv = BytesIO()
    handled = False
    command_prompt_matched = False
    matched_prompt_window = window_count = 0
    cache_socket_timeout = self._ssh_shell.gettimeout()
    command_timeout = self.get_option('persistent_command_timeout')
    self._validate_timeout_value(command_timeout, 'persistent_command_timeout')
    if (cache_socket_timeout != command_timeout):
        self._ssh_shell.settimeout(command_timeout)
    buffer_read_timeout = self.get_option('persistent_buffer_read_timeout')
    self._validate_timeout_value(buffer_read_timeout, 'persistent_buffer_read_timeout')
    while True:
        if command_prompt_matched:
            try:
                signal.signal(signal.SIGALRM, self._handle_buffer_read_timeout)
                signal.setitimer(signal.ITIMER_REAL, buffer_read_timeout)
                data = self._ssh_shell.recv(256)
                signal.alarm(0)
                command_prompt_matched = False
                signal.signal(signal.SIGALRM, self._handle_command_timeout)
                signal.alarm(command_timeout)
            except AnsibleCmdRespRecv:
                self._ssh_shell.settimeout(cache_socket_timeout)
                return self._command_response
        else:
            data = self._ssh_shell.recv(256)
        if (not data):
            break
        recv.write(data)
        offset = ((recv.tell() - 256) if (recv.tell() > 256) else 0)
        recv.seek(offset)
        window = self._strip(recv.read())
        window_count += 1
        if (prompts and (not handled)):
            handled = self._handle_prompt(window, prompts, answer, newline, False, check_all)
            matched_prompt_window = window_count
        elif (prompts and handled and prompt_retry_check and ((matched_prompt_window + 1) == window_count)):
            if self._handle_prompt(window, prompts, answer, newline, prompt_retry_check, check_all):
                raise AnsibleConnectionFailure(("For matched prompt '%s', answer is not valid" % self._matched_cmd_prompt))
        if self._find_prompt(window):
            self._last_response = recv.getvalue()
            resp = self._strip(self._last_response)
            self._command_response = self._sanitize(resp, command)
            if (buffer_read_timeout == 0.0):
                self._ssh_shell.settimeout(cache_socket_timeout)
                return self._command_response
            else:
                command_prompt_matched = True