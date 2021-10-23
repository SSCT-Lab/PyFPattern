def _connect(self):
    '\n        Connects to the remote device and starts the terminal\n        '
    if (not self.connected):
        self.paramiko_conn._set_log_channel(self._get_log_channel())
        self.paramiko_conn.force_persistence = self.force_persistence
        command_timeout = self.get_option('persistent_command_timeout')
        max_pause = min([self.get_option('persistent_connect_timeout'), command_timeout])
        retries = self.get_option('network_cli_retries')
        total_pause = 0
        for attempt in range((retries + 1)):
            try:
                ssh = self.paramiko_conn._connect()
                break
            except Exception as e:
                pause = (2 ** (attempt + 1))
                if ((attempt == retries) or (total_pause >= max_pause)):
                    raise AnsibleConnectionFailure(to_text(e, errors='surrogate_or_strict'))
                else:
                    msg = ('network_cli_retry: attempt: %d, caught exception(%s), pausing for %d seconds' % ((attempt + 1), to_text(e, errors='surrogate_or_strict'), pause))
                    self.queue_message('vv', msg)
                    time.sleep(pause)
                    total_pause += pause
                    continue
        self.queue_message('vvvv', 'ssh connection done, setting terminal')
        self._connected = True
        self._ssh_shell = ssh.ssh.invoke_shell()
        self._ssh_shell.settimeout(command_timeout)
        self.queue_message('vvvv', ('loaded terminal plugin for network_os %s' % self._network_os))
        terminal_initial_prompt = (self.get_option('terminal_initial_prompt') or self._terminal.terminal_initial_prompt)
        terminal_initial_answer = (self.get_option('terminal_initial_answer') or self._terminal.terminal_initial_answer)
        newline = (self.get_option('terminal_inital_prompt_newline') or self._terminal.terminal_inital_prompt_newline)
        check_all = (self.get_option('terminal_initial_prompt_checkall') or False)
        self.receive(prompts=terminal_initial_prompt, answer=terminal_initial_answer, newline=newline, check_all=check_all)
        self.queue_message('vvvv', 'firing event: on_open_shell()')
        self._terminal.on_open_shell()
        if (self._play_context.become and (self._play_context.become_method == 'enable')):
            self.queue_message('vvvv', 'firing event: on_become')
            auth_pass = self._play_context.become_pass
            self._terminal.on_become(passwd=auth_pass)
        self.queue_message('vvvv', 'ssh connection has completed successfully')
    return self