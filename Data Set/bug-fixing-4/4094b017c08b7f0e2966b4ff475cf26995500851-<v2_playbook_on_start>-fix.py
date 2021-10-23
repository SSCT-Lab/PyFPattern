def v2_playbook_on_start(self, playbook):
    self.playbook_name = os.path.basename(playbook._file_name)
    title = [('*Playbook initiated* (_%s_)' % self.guid)]
    invocation_items = []
    if (self._options and self.show_invocation):
        tags = self._options.tags
        skip_tags = self._options.skip_tags
        extra_vars = self._options.extra_vars
        subset = self._options.subset
        inventory = [os.path.abspath(i) for i in self._options.inventory]
        invocation_items.append(('Inventory:  %s' % ', '.join(inventory)))
        if (tags and (tags != ['all'])):
            invocation_items.append(('Tags:       %s' % ', '.join(tags)))
        if skip_tags:
            invocation_items.append(('Skip Tags:  %s' % ', '.join(skip_tags)))
        if subset:
            invocation_items.append(('Limit:      %s' % subset))
        if extra_vars:
            invocation_items.append(('Extra Vars: %s' % ' '.join(extra_vars)))
        title.append(('by *%s*' % self._options.remote_user))
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