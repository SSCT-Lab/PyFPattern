def handle_updated_workitem(self, data, integration):
    external_issue_key = data['resource']['workItemId']
    assigned_to = data['resource']['fields'].get('System.AssignedTo')
    status_change = data['resource']['fields'].get('System.State')
    project = data['resourceContainers']['project']['id']
    self.handle_assign_to(integration, external_issue_key, assigned_to)
    self.handle_status_change(integration, external_issue_key, status_change, project)