def _handle_prompt(self, resp, obj):
    prompt = re.compile(obj['prompt'], re.I)
    answer = obj['answer']
    match = prompt.search(resp)
    if match:
        self._shell.sendall(('%s\r' % answer))
        return True