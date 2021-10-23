

def _get_all_params_by_id(self, hid):
    url = ('%s/api/v2/hosts/%s' % (self.foreman_url, hid))
    ret = self._get_json(url, [404])
    if ((not ret) or (not isinstance(ret, MutableMapping)) or (not ret.get('all_parameters', False))):
        return {
            
        }
    return ret.get('all_parameters')
