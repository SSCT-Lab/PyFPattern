def test_alter_model_options_proxy(self):
    "Changing a proxy model's options should also make a change."
    before = self.make_project_state([self.author_proxy, self.author_empty])
    after = self.make_project_state([self.author_proxy_options, self.author_empty])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterModelOptions'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='authorproxy', options={
        'verbose_name': 'Super Author',
    })