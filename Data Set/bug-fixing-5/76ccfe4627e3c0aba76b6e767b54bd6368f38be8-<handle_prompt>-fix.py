def handle_prompt(self, resp, cmd):
    for prompt in to_list(cmd['prompt']):
        match = re.search(prompt, resp)
        if match:
            answer = ('%s\r' % cmd['response'])
            self.shell.sendall(answer)
            return True