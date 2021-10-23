

def query_resource_by_key(self, key, value, resource='regions', query_by='list', params=None, use_cache=False):
    if (not value):
        return {
            
        }
    if use_cache:
        if (resource in self.api_cache):
            if (self.api_cache[resource] and (self.api_cache[resource].get(key) == value)):
                return self.api_cache[resource]
    r_list = self.api_query(path=('/v1/%s/%s' % (resource, query_by)), data=params)
    if (not r_list):
        return {
            
        }
    for (r_id, r_data) in r_list.items():
        if (str(r_data[key]) == str(value)):
            self.api_cache.update({
                resource: r_data,
            })
            return r_data
    self.module.fail_json(msg=('Could not find %s with %s: %s' % (resource, key, value)))
