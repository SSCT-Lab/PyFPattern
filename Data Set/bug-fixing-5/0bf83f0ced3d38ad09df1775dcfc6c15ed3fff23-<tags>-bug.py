def tags(self, request, group, tag_list, **kwargs):
    if (not self.is_configured(request=request, project=group.project)):
        return tag_list
    prefix = self.get_conf_key()
    issue_id = GroupMeta.objects.get_value(group, ('%s:tid' % prefix))
    if (not issue_id):
        return tag_list
    tag_list.append(format_html('<a href="{}">{}</a>', self.get_issue_url(group, issue_id), self.get_issue_label(group, issue_id)))
    return tag_list