def get_host_variables(self, path, host):
    ' Runs <script> --host <hostname>, to determine additional host variables '
    cmd = [path, '--host', host]
    try:
        sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError as e:
        raise AnsibleError(('problem running %s (%s)' % (' '.join(cmd), e)))
    (out, err) = sp.communicate()
    if (out.strip() == ''):
        return {
            
        }
    try:
        return json_dict_bytes_to_unicode(self.loader.load(out))
    except ValueError:
        raise AnsibleError(('could not parse post variable response: %s, %s' % (cmd, out)))