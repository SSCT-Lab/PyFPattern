def _run(self, args, stdin=None, expected_rc=0):
    p = Popen(([self.cli_path] + args), stdout=PIPE, stderr=PIPE, stdin=PIPE)
    (out, err) = p.communicate(stdin)
    rc = p.wait()
    if (rc != expected_rc):
        raise LPassException(err)
    return (out, err)