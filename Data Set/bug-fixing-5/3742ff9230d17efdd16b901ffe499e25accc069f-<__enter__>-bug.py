def __enter__(self):
    self.sys_stdout = sys.stdout
    self.sys_stderr = sys.stderr
    sys.stdout = self.stdout = TextIOWrapper(BytesIO(), encoding=self.sys_stdout.encoding)
    sys.stderr = self.stderr = TextIOWrapper(BytesIO(), encoding=self.sys_stderr.encoding)
    return self