@override_settings(INSTALLED_APPS=['migrations.migrations_test_apps.mutate_state_a', 'migrations.migrations_test_apps.mutate_state_b'])
def test_unrelated_applied_migrations_mutate_state(self):
    '\n        #26647 - Unrelated applied migrations should be part of the final\n        state in both directions.\n        '
    executor = MigrationExecutor(connection)
    executor.migrate([('mutate_state_b', '0002_add_field')])
    executor.loader.build_graph()
    state = executor.migrate([('mutate_state_a', '0001_initial')])
    self.assertIn('added', dict(state.models[('mutate_state_b', 'b')].fields))
    executor.loader.build_graph()
    state = executor.migrate([('mutate_state_a', None)])
    self.assertIn('added', dict(state.models[('mutate_state_b', 'b')].fields))
    executor.migrate([('mutate_state_b', None)])