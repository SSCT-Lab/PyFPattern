def test_alter_model_options_proxy(self):
    "Changing a proxy model's options should also make a change."
    changes = self.get_changes([self.author_proxy, self.author_empty], [self.author_proxy_options, self.author_empty])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterModelOptions'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='authorproxy', options={
        'verbose_name': 'Super Author',
    })