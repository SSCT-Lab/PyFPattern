def __enter__(self):
    self.sys_stdout = sys.stdout
    self.sys_stderr = sys.stderr
    sys.stdout = self.stdout = AnsibleTextIOWrapper(BytesIO(), encoding=self.sys_stdout.encoding)
    sys.stderr = self.stderr = AnsibleTextIOWrapper(BytesIO(), encoding=self.sys_stderr.encoding)
    return self