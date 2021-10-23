def run(self):
    self.fetch(self.uri_meta)
    data = self._mangle_fields(self._data, self.uri_meta)
    data[(self._prefix % 'user-data')] = self._fetch(self.uri_user)
    data[(self._prefix % 'public-key')] = self._fetch(self.uri_ssh)
    self._data = {
        
    }
    self.fetch(self.uri_dynamic)
    dyndata = self._mangle_fields(self._data, self.uri_dynamic)
    data.update(dyndata)
    data = self.fix_invalid_varnames(data)
    if ('ansible_ec2_instance_identity_document_region' in data):
        data['ansible_ec2_placement_region'] = data['ansible_ec2_instance_identity_document_region']
    return data