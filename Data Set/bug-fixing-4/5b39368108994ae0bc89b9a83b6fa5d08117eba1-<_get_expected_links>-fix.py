def _get_expected_links(self):
    if (self.parameters.links is None):
        return None
    self.log('parameter links:')
    self.log(self.parameters.links, pretty_print=True)
    exp_links = []
    for (link, alias) in self.parameters.links:
        exp_links.append(('/%s:%s/%s' % (link, ('/' + self.parameters.name), alias)))
    return exp_links