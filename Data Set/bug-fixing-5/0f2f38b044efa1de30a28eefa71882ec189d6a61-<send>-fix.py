def send(self, command, prompt=None, answer=None, newline=True, sendonly=False, prompt_retry_check=False, check_all=False):
    '\n        Sends the command to the device in the opened shell\n        '
    if check_all:
        prompt_len = len(to_list(prompt))
        answer_len = len(to_list(answer))
        if (prompt_len != answer_len):
            raise AnsibleConnectionFailure(('Number of prompts (%s) is not same as that of answers (%s)' % (prompt_len, answer_len)))
    try:
        self._history.append(command)
        self._ssh_shell.sendall((b'%s\r' % command))
        if sendonly:
            return
        response = self.receive(command, prompt, answer, newline, prompt_retry_check, check_all)
        return to_text(response, errors='surrogate_or_strict')
    except (socket.timeout, AttributeError):
        display.vvvv(traceback.format_exc(), host=self._play_context.remote_addr)
        raise AnsibleConnectionFailure(('timeout value %s seconds reached while trying to send command: %s' % (self._ssh_shell.gettimeout(), command.strip())))