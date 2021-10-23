def test_new_model(self):
    'Tests autodetection of new models.'
    before = self.make_project_state([])
    after = self.make_project_state([self.other_pony_food])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'otherapp', 1)
    self.assertOperationTypes(changes, 'otherapp', 0, ['CreateModel'])
    self.assertOperationAttributes(changes, 'otherapp', 0, 0, name='Pony')
    self.assertEqual([name for (name, mgr) in changes['otherapp'][0].operations[0].managers], ['food_qs', 'food_mgr', 'food_mgr_kwargs'])