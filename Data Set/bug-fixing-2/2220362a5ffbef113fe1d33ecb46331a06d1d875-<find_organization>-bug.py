

def find_organization(self, name, **params):
    org = self._entities.Organization(self._server, name=name, **params)
    response = org.search(set(), {
        'search': 'name={}'.format(name),
    })
    if (len(response) == 1):
        return response[0]
    else:
        self._module.fail_json(msg=('No Content View found for %s' % name))
