def test_alter_model_options(self):
    "Changing a model's options should make a change."
    before = self.make_project_state([self.author_empty])
    after = self.make_project_state([self.author_with_options])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterModelOptions'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, options={
        'permissions': [('can_hire', 'Can hire')],
        'verbose_name': 'Authi',
    })
    before = self.make_project_state([self.author_with_options])
    after = self.make_project_state([self.author_empty])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterModelOptions'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='author', options={
        
    })