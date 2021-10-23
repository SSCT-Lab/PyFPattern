def get_pserver_programs(self, endpoint):
    '\n        Get pserver side main program and startup program for distributed training.\n\n        Args:\n            endpoint (str): current pserver endpoint.\n\n        Returns:\n            tuple: (main_program, startup_program), of type "Program"\n        '
    pserver_prog = self.get_pserver_program(endpoint)
    pserver_startup = self.get_startup_program(endpoint)
    return (pserver_prog, pserver_startup)