def get_organization_config(self):
    fields = [{
        'name': 'service_table',
        'type': 'table',
        'label': 'PagerDuty services with the Sentry integration enabled',
        'help': 'If a services needs to be updated, deleted, or added manually please do so here. Alert rules will need to be individually updated for any additions or deletions of services.',
        'addButtonText': '',
        'columnLabels': {
            'service': 'Service',
            'integration_key': 'Integration Key',
        },
        'columnKeys': ['service', 'integration_key'],
    }]
    return fields