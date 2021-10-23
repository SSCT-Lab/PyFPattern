

def _csrf_enabled(self):
    csrf_data = self._get_json_data(('%s/%s' % (self.url, 'api/json')), 'CSRF')
    if ('useCrumbs' not in csrf_data):
        self.module.fail_json(msg='Required fields not found in the Crumbs response.', details=csrf_data)
    return csrf_data['useCrumbs']
