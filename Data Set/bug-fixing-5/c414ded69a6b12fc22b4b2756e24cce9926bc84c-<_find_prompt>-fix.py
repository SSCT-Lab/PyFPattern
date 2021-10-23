def _find_prompt(self, response):
    for regex in self._terminal.terminal_errors_re:
        if regex.search(response):
            raise AnsibleConnectionFailure(response)
    for regex in self._terminal.terminal_prompts_re:
        match = regex.search(response)
        if match:
            self._matched_pattern = regex.pattern
            self._matched_prompt = match.group()
            return True