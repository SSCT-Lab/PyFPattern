def get_issue_display_name(self, external_issue):
    if (external_issue.metadata is None):
        return ''
    return external_issue.metadata['display_name']