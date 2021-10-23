def repository_set(self, params):
    product = self.find_product(params['product'], params['organization'])
    del params['product']
    del params['organization']
    if (not product):
        return False
    else:
        reposet = self._entities.RepositorySet(self._server, product=product, name=params['name'])
        reposet = reposet.search()[0]
        formatted_name = [params['name'].replace('(', '').replace(')', '')]
        formatted_name.append(params['basearch'])
        if params['releasever']:
            formatted_name.append(params['releasever'])
        formatted_name = ' '.join(formatted_name)
        repository = self._entities.Repository(self._server, product=product, name=formatted_name)
        repository._fields['organization'] = entity_fields.OneToOneField(entities.Organization)
        repository.organization = product.organization
        repository = repository.search()
        if (len(repository) == 0):
            reposet.enable(data={
                'basearch': params['basearch'],
                'releasever': params['releasever'],
            })
    return True