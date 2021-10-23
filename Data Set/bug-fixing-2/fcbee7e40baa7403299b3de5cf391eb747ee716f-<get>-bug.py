

def get(self):
    vhosts = self._exec(['list_vhosts', 'name', 'tracing'], True)
    for vhost in vhosts:
        (name, tracing) = vhost.split('\t')
        if (name == self.name):
            self._tracing = self.module.boolean(tracing)
            return True
    return False
