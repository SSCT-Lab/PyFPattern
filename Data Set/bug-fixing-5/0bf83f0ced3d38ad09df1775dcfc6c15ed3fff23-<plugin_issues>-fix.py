def plugin_issues(self, request, group, plugin_issues, **kwargs):
    if (not self.is_configured(request=request, project=group.project)):
        return plugin_issues
    item = {
        'slug': self.slug,
        'allowed_actions': self.allowed_actions,
        'title': self.get_title(),
    }
    issue = self.build_issue(group)
    if issue:
        item['issue'] = {
            'issue_id': issue.get('id'),
            'url': self._get_issue_url_compat(group, issue),
            'label': self._get_issue_label_compat(group, issue),
        }
    item.update(PluginSerializer(group.project).serialize(self, None, request.user))
    plugin_issues.append(item)
    return plugin_issues