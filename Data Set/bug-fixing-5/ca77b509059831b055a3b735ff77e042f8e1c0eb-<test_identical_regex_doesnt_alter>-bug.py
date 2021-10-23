def test_identical_regex_doesnt_alter(self):
    from_state = ModelState('testapp', 'model', [('id', models.AutoField(primary_key=True, validators=[RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')]))])
    to_state = ModelState('testapp', 'model', [('id', models.AutoField(primary_key=True, validators=[validate_slug]))])
    before = self.make_project_state([from_state])
    after = self.make_project_state([to_state])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertNumberMigrations(changes, 'testapp', 0)