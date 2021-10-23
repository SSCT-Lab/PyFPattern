@override_settings(AUTH_USER_MODEL='thirdapp.CustomUser')
def test_swappable(self):
    with isolate_lru_cache(apps.get_swappable_settings_name):
        before = self.make_project_state([self.custom_user])
        after = self.make_project_state([self.custom_user, self.author_with_custom_user])
        autodetector = MigrationAutodetector(before, after)
        changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='Author')
    self.assertMigrationDependencies(changes, 'testapp', 0, [('__setting__', 'AUTH_USER_MODEL')])