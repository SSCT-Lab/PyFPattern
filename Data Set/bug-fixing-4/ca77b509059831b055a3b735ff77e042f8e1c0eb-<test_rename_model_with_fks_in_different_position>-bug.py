def test_rename_model_with_fks_in_different_position(self):
    '\n        #24537 - Tests that the order of fields in a model does not influence\n        the RenameModel detection.\n        '
    before = self.make_project_state([ModelState('testapp', 'EntityA', [('id', models.AutoField(primary_key=True))]), ModelState('testapp', 'EntityB', [('id', models.AutoField(primary_key=True)), ('some_label', models.CharField(max_length=255)), ('entity_a', models.ForeignKey('testapp.EntityA', models.CASCADE))])])
    after = self.make_project_state([ModelState('testapp', 'EntityA', [('id', models.AutoField(primary_key=True))]), ModelState('testapp', 'RenamedEntityB', [('id', models.AutoField(primary_key=True)), ('entity_a', models.ForeignKey('testapp.EntityA', models.CASCADE)), ('some_label', models.CharField(max_length=255))])])
    autodetector = MigrationAutodetector(before, after, MigrationQuestioner({
        'ask_rename_model': True,
    }))
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, old_name='EntityB', new_name='RenamedEntityB')