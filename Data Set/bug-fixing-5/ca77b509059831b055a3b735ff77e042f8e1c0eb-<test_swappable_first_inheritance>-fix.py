def test_swappable_first_inheritance(self):
    'Tests that swappable models get their CreateModel first.'
    changes = self.get_changes([], [self.custom_user, self.aardvark])
    self.assertNumberMigrations(changes, 'thirdapp', 1)
    self.assertOperationTypes(changes, 'thirdapp', 0, ['CreateModel', 'CreateModel'])
    self.assertOperationAttributes(changes, 'thirdapp', 0, 0, name='CustomUser')
    self.assertOperationAttributes(changes, 'thirdapp', 0, 1, name='Aardvark')