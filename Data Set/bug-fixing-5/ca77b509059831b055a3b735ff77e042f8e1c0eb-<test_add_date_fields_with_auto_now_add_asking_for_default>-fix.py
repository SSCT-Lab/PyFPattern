@mock.patch('django.db.migrations.questioner.MigrationQuestioner.ask_auto_now_add_addition')
def test_add_date_fields_with_auto_now_add_asking_for_default(self, mocked_ask_method):
    changes = self.get_changes([self.author_empty], [self.author_dates_of_birth_auto_now_add])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AddField', 'AddField', 'AddField'])
    self.assertOperationFieldAttributes(changes, 'testapp', 0, 0, auto_now_add=True)
    self.assertOperationFieldAttributes(changes, 'testapp', 0, 1, auto_now_add=True)
    self.assertOperationFieldAttributes(changes, 'testapp', 0, 2, auto_now_add=True)
    self.assertEqual(mocked_ask_method.call_count, 3)