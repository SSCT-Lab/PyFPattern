

def v2_runner_on_ok(self, result):
    res = result._result
    module = result._task.action
    if ((module == 'setup') or ('ansible_facts' in res)):
        host = result._host.get_name()
        self.send_facts(host, res)
    else:
        self.append_result(result)
