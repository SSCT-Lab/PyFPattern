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
        if ('releasever' in params):
            formatted_name.append(params['releasever'])
        formatted_name = ' '.join(formatted_name)
        repository = self._entities.Repository(self._server, product=product, name=formatted_name)
        repository._fields['organization'] = entity_fields.OneToOneField(entities.Organization)
        repository.organization = product.organization
        repository = repository.search()
        if (len(repository) == 0):
            if ('releasever' in params):
                reposet.enable(data={
                    'basearch': params['basearch'],
                    'releasever': params['releasever'],
                })
            else:
                reposet.enable(data={
                    'basearch': params['basearch'],
                })
    return True