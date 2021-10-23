def notify(self, notification):
    event = notification.event
    group = event.group
    project = group.project
    org = group.organization
    subject = event.get_email_subject()
    link = group.get_absolute_url()
    template = 'sentry/emails/error.txt'
    html_template = 'sentry/emails/error.html'
    rules = []
    for rule in notification.rules:
        rule_link = reverse('sentry-edit-project-rule', args=[org.slug, project.slug, rule.id])
        rules.append((rule.label, rule_link))
    enhanced_privacy = org.flags.enhanced_privacy
    context = {
        'project_label': project.get_full_name(),
        'group': group,
        'event': event,
        'link': link,
        'rules': rules,
        'enhanced_privacy': enhanced_privacy,
    }
    if (not enhanced_privacy):
        interface_list = []
        for interface in six.itervalues(event.interfaces):
            body = interface.to_email_html(event)
            if (not body):
                continue
            text_body = interface.to_string(event)
            interface_list.append((interface.get_title(), mark_safe(body), text_body))
        context.update({
            'tags': event.get_tags(),
            'interfaces': interface_list,
        })
    headers = {
        'X-Sentry-Logger': group.logger,
        'X-Sentry-Logger-Level': group.get_level_display(),
        'X-Sentry-Team': project.team.slug,
        'X-Sentry-Project': project.slug,
        'X-Sentry-Reply-To': group_id_to_email(group.id),
    }
    for user_id in self.get_send_to(project):
        self.add_unsubscribe_link(context, user_id, project)
        self._send_mail(subject=subject, template=template, html_template=html_template, project=project, reference=group, headers=headers, type='notify.error', context=context, send_to=[user_id])