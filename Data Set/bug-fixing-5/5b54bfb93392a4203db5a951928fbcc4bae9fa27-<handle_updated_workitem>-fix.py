def handle_updated_workitem(self, data, integration):
    external_issue_key = data['resource']['workItemId']
    project = data['resourceContainers']['project']['id']
    try:
        assigned_to = data['resource']['fields'].get('System.AssignedTo')
        status_change = data['resource']['fields'].get('System.State')
    except KeyError:
        logger.info('vsts.updated-workitem-fields-not-passed', extra={
            'payload': data,
            'integration_id': integration.id,
        })
        return
    self.handle_assign_to(integration, external_issue_key, assigned_to)
    self.handle_status_change(integration, external_issue_key, status_change, project)