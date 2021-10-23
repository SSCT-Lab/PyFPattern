def list_jails(self):
    p = subprocess.Popen([self.jls_cmd, '-q', 'name'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    return to_text(stdout, errors='surrogate_or_strict').split()