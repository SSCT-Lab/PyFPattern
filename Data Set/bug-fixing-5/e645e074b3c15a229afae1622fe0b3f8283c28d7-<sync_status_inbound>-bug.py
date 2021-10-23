def sync_status_inbound(self, issue_key, data):
    affected_groups = list(Group.objects.get_groups_by_external_issue(self.model, issue_key).select_related('project'))
    groups_to_resolve = []
    groups_to_unresolve = []
    for group in affected_groups:
        should_resolve = self.should_resolve(data)
        should_unresolve = self.should_unresolve(data)
        if ((should_resolve is True) and (should_unresolve is True)):
            logger.warning('sync-config-conflict', extra={
                'organization_id': group.project.organization_id,
                'integration_id': self.model.id,
                'provider': self.model.get_provider(),
            })
            continue
        if should_unresolve:
            groups_to_unresolve.append(group)
        elif should_resolve:
            groups_to_resolve.append(group)
    if groups_to_resolve:
        self.update_group_status(groups_to_resolve, GroupStatus.RESOLVED, Activity.SET_RESOLVED)
    if groups_to_unresolve:
        self.update_group_status(groups_to_unresolve, GroupStatus.UNRESOLVED, Activity.SET_UNRESOLVED)