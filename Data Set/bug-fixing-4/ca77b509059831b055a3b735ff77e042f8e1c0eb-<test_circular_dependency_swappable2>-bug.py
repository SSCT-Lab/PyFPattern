@override_settings(AUTH_USER_MODEL='b.Tenant')
def test_circular_dependency_swappable2(self):
    '\n        #23322 - Tests that the dependency resolver knows to explicitly resolve\n        swappable models but with the swappable not being the first migrated\n        model.\n        '
    with isolate_lru_cache(apps.get_swappable_settings_name):
        address = ModelState('a', 'Address', [('id', models.AutoField(primary_key=True)), ('tenant', models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE))])
        tenant = ModelState('b', 'Tenant', [('id', models.AutoField(primary_key=True)), ('primary_address', models.ForeignKey('a.Address', models.CASCADE))], bases=(AbstractBaseUser,))
        before = self.make_project_state([])
        after = self.make_project_state([address, tenant])
        autodetector = MigrationAutodetector(before, after)
        changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'a', 2)
    self.assertOperationTypes(changes, 'a', 0, ['CreateModel'])
    self.assertOperationTypes(changes, 'a', 1, ['AddField'])
    self.assertMigrationDependencies(changes, 'a', 0, [])
    self.assertMigrationDependencies(changes, 'a', 1, [('__setting__', 'AUTH_USER_MODEL'), ('a', 'auto_1')])
    self.assertNumberMigrations(changes, 'b', 1)
    self.assertOperationTypes(changes, 'b', 0, ['CreateModel'])
    self.assertMigrationDependencies(changes, 'b', 0, [('a', 'auto_1')])