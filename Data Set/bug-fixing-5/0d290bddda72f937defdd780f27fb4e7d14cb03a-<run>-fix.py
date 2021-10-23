def run(self):
    result = {
        
    }
    filter = module.params.get('filter')
    if (not filter):
        for (key, path) in self.fact_paths.items():
            result[key] = self._fetch(((CS_METADATA_BASE_URL + '/') + path))
        result['cloudstack_user_data'] = self._get_user_data_json()
    elif (filter == 'cloudstack_user_data'):
        result['cloudstack_user_data'] = self._get_user_data_json()
    elif (filter in self.fact_paths):
        result[filter] = self._fetch(((CS_METADATA_BASE_URL + '/') + self.fact_paths[filter]))
    return result