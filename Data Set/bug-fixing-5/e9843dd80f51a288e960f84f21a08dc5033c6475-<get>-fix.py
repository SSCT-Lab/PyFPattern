def get(self, request):
    org = Organization(id=1, slug='organization', name='My Company')
    project = Project(id=1, organization=org, slug='project', name='My Project')
    group = Group(id=1, project=project)
    return MailPreview(html_template='sentry/emails/activity/new-user-feedback.html', text_template='sentry/emails/activity/new-user-feedback.txt', context={
        'group': group,
        'report': {
            'name': 'Homer Simpson',
            'email': 'homer.simpson@example.com',
            'comments': 'I hit a bug.\n\nI went to https://example.com, hit the any key, and then it stopped working. DOH!',
        },
    }).render(request)