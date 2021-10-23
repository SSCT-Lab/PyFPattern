def v2_playbook_on_notify(self, handler, host):
    if (self._display.verbosity > 1):
        self._display.display(('NOTIFIED HANDLER %s for %s' % (handler.get_name(), host)), color=C.COLOR_VERBOSE, screen_only=True)