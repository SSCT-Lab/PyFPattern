def _run(self, args, expected_rc=0, command_input=None, ignore_errors=False):
    command = ([self.cli_path] + args)
    p = Popen(command, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    (out, err) = p.communicate(input=command_input)
    rc = p.wait()
    if ((not ignore_errors) and (rc != expected_rc)):
        raise AnsibleModuleError(to_native(err))
    return (rc, out, err)