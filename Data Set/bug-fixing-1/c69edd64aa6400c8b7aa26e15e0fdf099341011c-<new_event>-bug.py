

@login_required
def new_event(request):
    platform = request.GET.get('platform', 'python')
    org = Organization(id=1, slug='example', name='Example')
    team = Team(id=1, slug='example', name='Example', organization=org)
    project = Project(id=1, slug='example', name='Example', team=team, organization=org)
    group = Group(id=1, project=project, message='This is an example event.', level=logging.ERROR)
    event = Event(id=1, project=project, group=group, message=group.message, data=load_data(platform))
    rule = Rule(label='An example rule')
    interface_list = []
    for interface in event.interfaces.itervalues():
        body = interface.to_email_html(event)
        if (not body):
            continue
        interface_list.append((interface.get_title(), mark_safe(body)))
    return MailPreview(html_template='sentry/emails/error.html', text_template='sentry/emails/error.html', context={
        'rule': rule,
        'group': group,
        'event': event,
        'link': 'http://example.com/link',
        'interfaces': interface_list,
        'tags': event.get_tags(),
        'project_label': project.name,
    }).render()
