def _handle_prompt(self, resp, obj):
    'Matches the command prompt and responds'
    if (not isinstance(obj['prompt'], list)):
        obj['prompt'] = [obj['prompt']]
    prompts = [re.compile(r, re.I) for r in obj['prompt']]
    answer = obj['answer']
    for regex in prompts:
        match = regex.search(resp)
        if match:
            self._shell.sendall(('%s\r' % answer))
            return True