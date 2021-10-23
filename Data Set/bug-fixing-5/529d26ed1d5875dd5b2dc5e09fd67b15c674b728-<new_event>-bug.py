@login_required
def new_event(request):
    platform = request.GET.get('platform', 'python')
    org = Organization(id=1, slug='example', name='Example')
    team = Team(id=1, slug='example', name='Example', organization=org)
    project = Project(id=1, slug='example', name='Example', team=team, organization=org)
    random = get_random(request)
    group = next(make_group_generator(random, project))
    event = Event(id=1, project=project, group=group, message=group.message, data=load_data(platform), datetime=to_datetime(random.randint(to_timestamp(group.first_seen), to_timestamp(group.last_seen))))
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
        'tags': [('logger', 'javascript'), ('environment', 'prod'), ('level', 'error'), ('device', 'Other')],
    }).render(request)