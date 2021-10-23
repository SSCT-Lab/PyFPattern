def delete_tenant(self, tenant):
    ' Deletes a tenant from manageiq.\n\n        Returns:\n            dict with `msg` and `changed`\n        '
    try:
        url = ('%s/tenants/%s' % (self.api_url, tenant['id']))
        result = self.client.post(url, action='delete')
    except Exception as e:
        self.module.fail_json(msg=('failed to delete tenant %s: %s' % (tenant['name'], str(e))))
    if (result['success'] is False):
        self.module.fail_json(msg=result['message'])
    return dict(changed=True, msg=result['message'])