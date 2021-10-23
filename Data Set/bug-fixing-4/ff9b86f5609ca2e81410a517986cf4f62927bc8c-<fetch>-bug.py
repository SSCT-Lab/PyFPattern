def fetch(self, uri, recurse=True):
    raw_subfields = self._fetch(uri)
    if (not raw_subfields):
        return
    subfields = raw_subfields.split('\n')
    for field in subfields:
        if (field.endswith('/') and recurse):
            self.fetch((uri + field))
        if uri.endswith('/'):
            new_uri = (uri + field)
        else:
            new_uri = ((uri + '/') + field)
        if ((new_uri not in self._data) and (not new_uri.endswith('/'))):
            content = self._fetch(new_uri)
            if ((field == 'security-groups') or (field == 'security-group-ids')):
                sg_fields = ','.join(content.split('\n'))
                self._data[('%s' % new_uri)] = sg_fields
            else:
                try:
                    dict = json.loads(content)
                    self._data[('%s' % new_uri)] = content
                    for (key, value) in dict.items():
                        self._data[('%s_%s' % (new_uri, key.lower()))] = value
                except:
                    self._data[('%s' % new_uri)] = content