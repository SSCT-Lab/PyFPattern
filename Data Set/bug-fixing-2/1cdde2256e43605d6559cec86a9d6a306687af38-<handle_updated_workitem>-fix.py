

def handle_updated_workitem(self, data, integration):
    try:
        external_issue_key = data['resource']['workItemId']
        project = data['resourceContainers']['project']['id']
    except KeyError as e:
        logger.info('vsts.updating-workitem-does-not-have-necessary-information', extra={
            'error': six.text_type(e),
            'integration_id': integration.id,
        })
    try:
        assigned_to = data['resource']['fields'].get('System.AssignedTo')
        status_change = data['resource']['fields'].get('System.State')
    except KeyError as e:
        logger.info('vsts.updated-workitem-fields-not-passed', extra={
            'error': six.text_type(e),
            'workItemId': data['resource']['workItemId'],
            'integration_id': integration.id,
        })
        return
    self.handle_assign_to(integration, external_issue_key, assigned_to)
    self.handle_status_change(integration, external_issue_key, status_change, project)
