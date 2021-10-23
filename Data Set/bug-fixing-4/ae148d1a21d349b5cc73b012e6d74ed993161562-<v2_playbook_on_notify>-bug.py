def v2_playbook_on_notify(self, handler, host):
    self._display.vv(('NOTIFIED HANDLER %s for %s' % (handler.get_name(), host)))