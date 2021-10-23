def actionOptionalLimitSet(self, to, *args, **kwargs):
    if (not config.multiuser_local):
        self.cmd('notification', ['info', 'This function is disabled on this proxy'])
    else:
        return super(UiWebsocketPlugin, self).actionOptionalLimitSet(to, *args, **kwargs)