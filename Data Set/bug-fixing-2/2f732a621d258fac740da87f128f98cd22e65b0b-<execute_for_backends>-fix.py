

def execute_for_backends(self, cmd, pxname, svname, wait_for_status=None):
    '\n        Run some command on the specified backends. If no backends are provided they will\n        be discovered automatically (all backends)\n        '
    if (pxname is None):
        backends = self.discover_all_backends()
    else:
        backends = [pxname]
    for backend in backends:
        state = self.get_state_for(backend, svname)
        if (self.fail_on_not_found and (state is None)):
            self.module.fail_json(msg=("The specified backend '%s/%s' was not found!" % (backend, svname)))
        if (state is not None):
            self.execute(Template(cmd).substitute(pxname=backend, svname=svname))
            if self.wait:
                self.wait_until_status(backend, svname, wait_for_status)
