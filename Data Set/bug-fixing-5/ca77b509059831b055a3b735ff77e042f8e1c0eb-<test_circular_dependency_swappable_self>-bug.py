@override_settings(AUTH_USER_MODEL='a.Person')
def test_circular_dependency_swappable_self(self):
    '\n        #23322 - Tests that the dependency resolver knows to explicitly resolve\n        swappable models.\n        '
    with isolate_lru_cache(apps.get_swappable_settings_name):
        person = ModelState('a', 'Person', [('id', models.AutoField(primary_key=True)), ('parent1', models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='children'))])
        before = self.make_project_state([])
        after = self.make_project_state([person])
        autodetector = MigrationAutodetector(before, after)
        changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'a', 1)
    self.assertOperationTypes(changes, 'a', 0, ['CreateModel'])
    self.assertMigrationDependencies(changes, 'a', 0, [])