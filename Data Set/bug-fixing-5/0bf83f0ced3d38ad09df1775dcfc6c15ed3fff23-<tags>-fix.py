def tags(self, request, group, tag_list, **kwargs):
    if (not self.is_configured(request=request, project=group.project)):
        return tag_list
    issue = self.build_issue(group)
    if (not issue):
        return tag_list
    tag_list.append(format_html('<a href="{}">{}</a>', self._get_issue_url_compat(group, issue), self._get_issue_label_compat(group, issue)))
    return tag_list