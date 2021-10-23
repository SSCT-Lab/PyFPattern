def handle_prompt(self, resp, cmd):
    prompt = to_list(cmd['prompt'])
    response = to_list(cmd['response'])
    for (pr, ans) in zip(prompt, response):
        match = pr.search(resp)
        if match:
            answer = ('%s\r' % ans)
            self.shell.sendall(answer)
            return True