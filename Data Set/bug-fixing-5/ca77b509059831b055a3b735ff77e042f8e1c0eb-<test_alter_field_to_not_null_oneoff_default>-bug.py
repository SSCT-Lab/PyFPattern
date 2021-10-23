@mock.patch('django.db.migrations.questioner.MigrationQuestioner.ask_not_null_alteration', return_value='Some Name')
def test_alter_field_to_not_null_oneoff_default(self, mocked_ask_method):
    '\n        #23609 - Tests autodetection of nullable to non-nullable alterations.\n        '
    before = self.make_project_state([self.author_name_null])
    after = self.make_project_state([self.author_name])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertEqual(mocked_ask_method.call_count, 1)
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['AlterField'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='name', preserve_default=False)
    self.assertOperationFieldAttributes(changes, 'testapp', 0, 0, default='Some Name')