

def build_dynamic_field(self, group, field_meta):
    "\n        Builds a field based on Jira's meta field information\n        "
    schema = field_meta['schema']
    fieldtype = 'text'
    fkwargs = {
        'label': field_meta['name'],
        'required': field_meta['required'],
    }
    if ((schema['type'] in ['securitylevel', 'priority']) or (schema.get('custom') == JIRA_CUSTOM_FIELD_TYPES['select'])):
        fieldtype = 'select'
        fkwargs['choices'] = self.make_choices(field_meta.get('allowedValues'))
    elif (field_meta.get('autoCompleteUrl') and ((schema.get('items') == 'user') or (schema['type'] == 'user'))):
        fieldtype = 'select'
        sentry_url = self.search_url(group.organization.slug)
        fkwargs['url'] = ('%s?jira_url=%s' % (sentry_url, quote_plus(field_meta['autoCompleteUrl'])))
        fkwargs['choices'] = []
    elif (schema['type'] in ['timetracking']):
        return None
    elif (schema.get('items') in ['worklog', 'attachment']):
        return None
    elif ((schema['type'] == 'array') and (schema['items'] != 'string')):
        fieldtype = 'select'
        fkwargs.update({
            'multiple': True,
            'choices': self.make_choices(field_meta.get('allowedValues')),
            'default': [],
        })
    if schema.get('custom'):
        if (schema['custom'] == JIRA_CUSTOM_FIELD_TYPES['textarea']):
            fieldtype = 'textarea'
    fkwargs['type'] = fieldtype
    return fkwargs
