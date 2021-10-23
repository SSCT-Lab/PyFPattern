def test_rename_m2m_through_model(self):
    '\n        Tests autodetection of renamed models that are used in M2M relations as\n        through models.\n        '
    before = self.make_project_state([self.author_with_m2m_through, self.publisher, self.contract])
    after = self.make_project_state([self.author_with_renamed_m2m_through, self.publisher, self.contract_renamed])
    autodetector = MigrationAutodetector(before, after, MigrationQuestioner({
        'ask_rename_model': True,
    }))
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, old_name='Contract', new_name='Deal')