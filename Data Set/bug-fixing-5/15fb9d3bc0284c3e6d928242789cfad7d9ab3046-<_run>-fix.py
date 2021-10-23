def _run(self, args, stdin=None, expected_rc=0):
    p = Popen(([self.cli_path] + args), stdout=PIPE, stderr=PIPE, stdin=PIPE)
    (out, err) = p.communicate(to_bytes(stdin))
    rc = p.wait()
    if (rc != expected_rc):
        raise LPassException(err)
    return (to_text(out, errors='surrogate_or_strict'), to_text(err, errors='surrogate_or_strict'))