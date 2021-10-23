@mock.patch('django.db.migrations.questioner.MigrationQuestioner.ask_not_null_addition', side_effect=AssertionError('Should not have prompted for not null addition'))
def test_add_many_to_many(self, mocked_ask_method):
    '#22435 - Adding a ManyToManyField should not prompt for a default.'
    before = self.make_project_state([self.author_empty, self.publisher])
    after = self.make_project_state([self.author_with_m2m, self.publisher])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AddField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='publishers')