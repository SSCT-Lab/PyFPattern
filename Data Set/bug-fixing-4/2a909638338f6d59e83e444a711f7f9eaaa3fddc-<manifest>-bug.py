def manifest(self, params):
    org = self.find_organization(params['organization'])
    params['organization'] = org.id
    try:
        file = open((os.getcwd() + params['content']), 'r')
        content = file.read()
    finally:
        file.close()
    manifest = self._entities.Subscription(self._server)
    try:
        manifest.upload(data={
            'organization_id': org.id,
        }, files={
            'content': content,
        })
        return True
    except Exception:
        e = get_exception()
        if ('Import is the same as existing data' in e.message):
            return True
        else:
            self._module.fail_json(msg=('Manifest import failed with %s' % e))