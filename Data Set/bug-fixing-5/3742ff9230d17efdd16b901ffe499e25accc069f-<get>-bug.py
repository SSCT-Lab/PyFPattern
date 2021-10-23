def get(self):
    'Return ``(stdout, stderr)``'
    return (self.stdout.getvalue(), self.stderr.getvalue())