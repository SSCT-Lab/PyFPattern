def get_create_issue_config(self, group, **kwargs):
    fields = super(JiraIntegration, self).get_create_issue_config(group, **kwargs)
    params = kwargs.get('params', {
        
    })
    client = self.get_client()
    try:
        resp = client.get_create_meta(params.get('project'))
    except ApiUnauthorized:
        raise IntegrationError('Jira returned: Unauthorized. Please check your configuration settings.')
    try:
        meta = resp['projects'][0]
    except IndexError:
        raise IntegrationError('Error in Jira configuration, no projects found.')
    issue_type = params.get('issuetype')
    issue_type_meta = self.get_issue_type_meta(issue_type, meta)
    issue_type_choices = self.make_choices(meta['issuetypes'])
    if issue_type:
        if (not any((c for c in issue_type_choices if (c[0] == issue_type)))):
            issue_type = issue_type_meta['id']
    fields = (([{
        'name': 'project',
        'label': 'Jira Project',
        'choices': [(p['id'], p['key']) for p in client.get_projects_list()],
        'default': meta['id'],
        'type': 'select',
        'updatesForm': True,
    }] + fields) + [{
        'name': 'issuetype',
        'label': 'Issue Type',
        'default': (issue_type or issue_type_meta['id']),
        'type': 'select',
        'choices': issue_type_choices,
        'updatesForm': True,
    }])
    standard_fields = ([f['name'] for f in fields] + ['summary'])
    ignored_fields = set()
    anti_gravity = {
        'priority': (- 150),
        'fixVersions': (- 125),
        'components': (- 100),
        'security': (- 50),
    }
    dynamic_fields = issue_type_meta.get('fields').keys()
    dynamic_fields.sort(key=(lambda f: (anti_gravity.get(f) or 0)))
    for field in dynamic_fields:
        if ((field in standard_fields) or (field in [x.strip() for x in ignored_fields])):
            continue
        mb_field = self.build_dynamic_field(group, issue_type_meta['fields'][field])
        if mb_field:
            mb_field['name'] = field
            fields.append(mb_field)
    for field in fields:
        if (field['name'] == 'priority'):
            field['choices'] = self.make_choices(client.get_priorities())
            field['default'] = ''
        elif (field['name'] == 'fixVersions'):
            field['choices'] = self.make_choices(client.get_versions(meta['key']))
    return fields