

def _handle_prompt(self, resp, obj):
    'Matches the command prompt and responds'
    prompt = re.compile(obj['prompt'], re.I)
    answer = obj['answer']
    match = prompt.search(resp)
    if match:
        self._shell.sendall(('%s\r' % answer))
        return True
