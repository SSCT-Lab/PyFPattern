def test_many_to_many_changed_to_concrete_field(self):
    '\n        #23938 - Tests that changing a ManyToManyField into a concrete field\n        first removes the m2m field and then adds the concrete field.\n        '
    before = self.make_project_state([self.author_with_m2m, self.publisher])
    after = self.make_project_state([self.author_with_former_m2m])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RemoveField', 'AddField', 'DeleteModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='publishers', model_name='author')
    self.assertOperationAttributes(changes, 'testapp', 0, 1, name='publishers', model_name='author')
    self.assertOperationAttributes(changes, 'testapp', 0, 2, name='Publisher')
    self.assertOperationFieldAttributes(changes, 'testapp', 0, 1, max_length=100)