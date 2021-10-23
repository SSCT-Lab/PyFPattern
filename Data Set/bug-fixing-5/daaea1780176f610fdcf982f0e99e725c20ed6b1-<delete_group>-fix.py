def delete_group(self, group):
    ' Deletes a group from manageiq.\n\n        Returns:\n            a dict of:\n            changed: boolean indicating if the entity was updated.\n            msg: a short message describing the operation executed.\n        '
    try:
        url = ('%s/groups/%s' % (self.api_url, group['id']))
        result = self.client.post(url, action='delete')
    except Exception as e:
        self.module.fail_json(msg=('failed to delete group %s: %s' % (group['description'], str(e))))
    if (result['success'] is False):
        self.module.fail_json(msg=result['message'])
    return dict(changed=True, msg=('deleted group %s with id %i' % (group['description'], group['id'])))