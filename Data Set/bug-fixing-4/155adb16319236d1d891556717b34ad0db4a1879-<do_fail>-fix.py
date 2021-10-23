def do_fail(self, module):
    module.fail_json(msg=self.msg, other=self.module_fail_args)