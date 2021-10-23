def test_proxy(self):
    'Tests that the autodetector correctly deals with proxy models.'
    before = self.make_project_state([self.author_empty])
    after = self.make_project_state([self.author_empty, self.author_proxy])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='AuthorProxy', options={
        'proxy': True,
    })
    before = self.make_project_state([self.author_empty, self.author_proxy])
    after = self.make_project_state([self.author_empty, self.author_proxy_notproxy])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['DeleteModel', 'CreateModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='AuthorProxy')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='AuthorProxy', options={
        
    })