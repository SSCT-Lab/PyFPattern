def test_alter_model_managers(self):
    '\n        Tests that changing the model managers adds a new operation.\n        '
    changes = self.get_changes([self.other_pony], [self.other_pony_food])
    self.assertNumberMigrations(changes, 'otherapp', 1)
    self.assertOperationTypes(changes, 'otherapp', 0, ['AlterModelManagers'])
    self.assertOperationAttributes(changes, 'otherapp', 0, 0, name='pony')
    self.assertEqual([name for (name, mgr) in changes['otherapp'][0].operations[0].managers], ['food_qs', 'food_mgr', 'food_mgr_kwargs'])
    self.assertEqual(changes['otherapp'][0].operations[0].managers[1][1].args, ('a', 'b', 1, 2))
    self.assertEqual(changes['otherapp'][0].operations[0].managers[2][1].args, ('x', 'y', 3, 4))