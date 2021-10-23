def _find_prompt(self, response):
    'Searches the buffered response for a matching command prompt\n        '
    errored_response = None
    is_error_message = False
    for regex in self._terminal.terminal_stderr_re:
        if regex.search(response):
            is_error_message = True
            for regex in self._terminal.terminal_stdout_re:
                match = regex.search(response)
                if match:
                    errored_response = response
                    self._matched_prompt = match.group()
                    break
    if (not is_error_message):
        for regex in self._terminal.terminal_stdout_re:
            match = regex.search(response)
            if match:
                self._matched_pattern = regex.pattern
                self._matched_prompt = match.group()
                if (not errored_response):
                    return True
    if errored_response:
        raise AnsibleConnectionFailure(errored_response)
    return False