def get(self):
    'Return ``(stdout, stderr)``'
    return (self.stdout.buffer.getvalue(), self.stderr.buffer.getvalue())