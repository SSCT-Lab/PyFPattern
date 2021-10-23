

def v2_playbook_on_notify(self, result, handler):
    host = result._host.get_name()
    self.playbook_on_notify(host, handler)
