def run(self, terms, variables, **kwargs):
    if (not HAVE_REDIS):
        raise AnsibleError("Can't LOOKUP(redis_kv): module redis is not installed")
    self.set_options(direct=kwargs)
    host = self.get_option('host')
    port = self.get_option('port')
    socket = self.get_option('socket')
    if (socket is None):
        conn = redis.Redis(host=host, port=port)
    else:
        conn = redis.Redis(unix_socket_path=socket)
    ret = []
    for term in terms:
        try:
            res = conn.get(term)
            if (res is None):
                res = ''
            ret.append(res)
        except Exception:
            ret.append('')
    return ret