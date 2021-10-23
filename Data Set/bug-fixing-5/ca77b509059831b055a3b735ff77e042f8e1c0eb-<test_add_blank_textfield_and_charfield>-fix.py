@mock.patch('django.db.migrations.questioner.MigrationQuestioner.ask_not_null_addition', side_effect=AssertionError('Should not have prompted for not null addition'))
def test_add_blank_textfield_and_charfield(self, mocked_ask_method):
    '\n        #23405 - Adding a NOT NULL and blank `CharField` or `TextField`\n        without default should not prompt for a default.\n        '
    changes = self.get_changes([self.author_empty], [self.author_with_biography_blank])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AddField', 'AddField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0)