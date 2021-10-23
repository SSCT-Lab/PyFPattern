def v2_playbook_on_start(self, playbook):
    self.playbook_name = os.path.basename(playbook._file_name)
    title = [('*Playbook initiated* (_%s_)' % self.guid)]
    invocation_items = []
    if (self._plugin_options and self.show_invocation):
        tags = self.get_option('tags')
        skip_tags = self.get_option('skip_tags')
        extra_vars = self.get_option('extra_vars')
        subset = self.get_option('subset')
        inventory = os.path.basename(os.path.realpath(self.get_option('inventory')))
        invocation_items.append(('Inventory:  %s' % inventory))
        if (tags and (tags != 'all')):
            invocation_items.append(('Tags:       %s' % tags))
        if skip_tags:
            invocation_items.append(('Skip Tags:  %s' % skip_tags))
        if subset:
            invocation_items.append(('Limit:      %s' % subset))
        if extra_vars:
            invocation_items.append(('Extra Vars: %s' % ' '.join(extra_vars)))
        title.append(('by *%s*' % self.get_option('remote_user')))
    title.append(('\n\n*%s*' % self.playbook_name))
    msg_items = [' '.join(title)]
    if invocation_items:
        msg_items.append(('```\n%s\n```' % '\n'.join(invocation_items)))
    msg = '\n'.join(msg_items)
    attachments = [{
        'fallback': msg,
        'fields': [{
            'value': msg,
        }],
        'color': 'warning',
        'mrkdwn_in': ['text', 'fallback', 'fields'],
    }]
    self.send_msg(attachments=attachments)