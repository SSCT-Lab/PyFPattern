def get_create_issue_config(self, group, **kwargs):
    kwargs['link_referrer'] = 'jira_integration'
    fields = super(JiraIntegration, self).get_create_issue_config(group, **kwargs)
    params = kwargs.get('params', {
        
    })
    defaults = self.get_project_defaults(group.project_id)
    project_id = params.get('project', defaults.get('project'))
    client = self.get_client()
    try:
        jira_projects = client.get_projects_list()
    except ApiError as exc:
        logger.info('jira.get-create-issue-config.no-projects', extra={
            'integration_id': self.model.id,
            'organization_id': self.organization_id,
            'error': exc.message,
        })
        raise IntegrationError('Could not fetch project list from JiraEnsure that jira is available and your account is still active.')
    meta = self.get_issue_create_meta(client, project_id, jira_projects)
    if (not meta):
        raise IntegrationError('Could not fetch issue create metadata from Jira. Ensure that the integration user has access to the requested project.')
    issue_type = params.get('issuetype', defaults.get('issuetype'))
    issue_type_meta = self.get_issue_type_meta(issue_type, meta)
    issue_type_choices = self.make_choices(meta['issuetypes'])
    if issue_type:
        if (not any((c for c in issue_type_choices if (c[0] == issue_type)))):
            issue_type = issue_type_meta['id']
    fields = (([{
        'name': 'project',
        'label': 'Jira Project',
        'choices': [(p['id'], p['key']) for p in jira_projects],
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
    ignored_fields = set((k for (k, v) in six.iteritems(issue_type_meta['fields']) if (v['name'] in HIDDEN_ISSUE_FIELDS['names'])))
    ignored_fields.update(HIDDEN_ISSUE_FIELDS['keys'])
    anti_gravity = {
        'priority': (- 150),
        'fixVersions': (- 125),
        'components': (- 100),
        'security': (- 50),
    }
    dynamic_fields = issue_type_meta['fields'].keys()
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
            field['default'] = defaults.get('priority', '')
        elif (field['name'] == 'fixVersions'):
            field['choices'] = self.make_choices(client.get_versions(meta['key']))
        elif (field['name'] == 'labels'):
            field['default'] = defaults.get('labels', '')
    return fields