def test_proxy(self):
    'Tests that the autodetector correctly deals with proxy models.'
    changes = self.get_changes([self.author_empty], [self.author_empty, self.author_proxy])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='AuthorProxy', options={
        'proxy': True,
    })
    changes = self.get_changes([self.author_empty, self.author_proxy], [self.author_empty, self.author_proxy_notproxy])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['DeleteModel', 'CreateModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='AuthorProxy')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='AuthorProxy', options={
        
    })