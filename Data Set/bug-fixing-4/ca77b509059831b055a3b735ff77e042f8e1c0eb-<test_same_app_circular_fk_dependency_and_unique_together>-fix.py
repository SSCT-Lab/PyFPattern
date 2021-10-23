def test_same_app_circular_fk_dependency_and_unique_together(self):
    '\n        #22275 - Tests that a migration with circular FK dependency does not try\n        to create unique together constraint before creating all required fields\n        first.\n        '
    changes = self.get_changes([], [self.knight, self.rabbit])
    self.assertNumberMigrations(changes, 'eggs', 1)
    self.assertOperationTypes(changes, 'eggs', 0, ['CreateModel', 'CreateModel', 'AlterUniqueTogether'])
    self.assertNotIn('unique_together', changes['eggs'][0].operations[0].options)
    self.assertNotIn('unique_together', changes['eggs'][0].operations[1].options)
    self.assertMigrationDependencies(changes, 'eggs', 0, [])