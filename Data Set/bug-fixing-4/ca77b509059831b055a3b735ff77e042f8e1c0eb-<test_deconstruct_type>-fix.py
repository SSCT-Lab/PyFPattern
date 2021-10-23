def test_deconstruct_type(self):
    '\n        #22951 -- Uninstantiated classes with deconstruct are correctly returned\n        by deep_deconstruct during serialization.\n        '
    author = ModelState('testapp', 'Author', [('id', models.AutoField(primary_key=True)), ('name', models.CharField(max_length=200, default=models.IntegerField))])
    changes = self.get_changes([], [author])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel'])