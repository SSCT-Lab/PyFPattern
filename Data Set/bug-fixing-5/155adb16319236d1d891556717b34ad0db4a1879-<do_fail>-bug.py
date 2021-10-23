def do_fail(self, module):
    module.fail_json(msg=self.msg, **self.args)