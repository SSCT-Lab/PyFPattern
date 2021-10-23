def get_trainer_program(self, wait_port=True):
    '\n        Get transpiled trainer side program.\n\n        Returns:\n            Program: trainer side program.\n        '
    lr_ops = self._get_lr_ops()
    delete_ops(self.origin_program.global_block(), self.optimize_ops)
    delete_ops(self.origin_program.global_block(), lr_ops)
    self.origin_program.__str__()
    if wait_port:
        wait_server_ready(self.pserver_endpoints)
    return self.origin_program