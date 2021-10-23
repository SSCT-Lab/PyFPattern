def test_proxy_bases_first(self):
    'Tests that bases of proxies come first.'
    changes = self.get_changes([], [self.author_empty, self.author_proxy, self.author_proxy_proxy])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel', 'CreateModel', 'CreateModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='Author')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='AuthorProxy')
    self.assertOperationAttributes(changes, 'testapp', 0, 2, name='AAuthorProxyProxy')