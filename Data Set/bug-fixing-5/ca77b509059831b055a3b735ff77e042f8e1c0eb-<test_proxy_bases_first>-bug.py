def test_proxy_bases_first(self):
    'Tests that bases of proxies come first.'
    before = self.make_project_state([])
    after = self.make_project_state([self.author_empty, self.author_proxy, self.author_proxy_proxy])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel', 'CreateModel', 'CreateModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='Author')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='AuthorProxy')
    self.assertOperationAttributes(changes, 'testapp', 0, 2, name='AAuthorProxyProxy')