def run(self, terms, variables, **kwargs):
    ret = []
    for term in terms:
        p = subprocess.Popen(term, cwd=self._loader.get_basedir(), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        (stdout, stderr) = p.communicate()
        if (p.returncode == 0):
            ret.extend(stdout.splitlines())
        else:
            raise AnsibleError(('lookup_plugin.lines(%s) returned %d' % (term, p.returncode)))
    return ret