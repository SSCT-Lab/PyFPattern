

def _handle_prompt(self, resp, prompts, answer, newline, prompt_retry_check=False, check_all=False):
    '\n        Matches the command prompt and responds\n\n        :arg resp: Byte string containing the raw response from the remote\n        :arg prompts: Sequence of byte strings that we consider prompts for input\n        :arg answer: Sequence of Byte string to send back to the remote if we find a prompt.\n                A carriage return is automatically appended to this string.\n        :param prompt_retry_check: Bool value for trying to detect more prompts\n        :param check_all: Bool value to indicate if all the values in prompt sequence should be matched or any one of\n                          given prompt.\n        :returns: True if a prompt was found in ``resp``. If check_all is True\n                  will True only after all the prompt in the prompts list are matched. False otherwise.\n        '
    single_prompt = False
    if (not isinstance(prompts, list)):
        prompts = [prompts]
        single_prompt = True
    if (not isinstance(answer, list)):
        answer = [answer]
    prompts_regex = [re.compile(r, re.I) for r in prompts]
    for (index, regex) in enumerate(prompts_regex):
        match = regex.search(resp)
        if match:
            self._matched_cmd_prompt = match.group()
            self._log_messages(('matched command prompt: %s' % self._matched_cmd_prompt))
            if (not prompt_retry_check):
                prompt_answer = (answer[index] if (len(answer) > index) else answer[0])
                self._ssh_shell.sendall((b'%s' % prompt_answer))
                if newline:
                    self._ssh_shell.sendall(b'\r')
                    prompt_answer += '\r'
                self._log_messages(('matched command prompt answer: %s' % prompt_answer))
            if (check_all and prompts and (not single_prompt)):
                prompts.pop(0)
                answer.pop(0)
                return False
            return True
    return False
