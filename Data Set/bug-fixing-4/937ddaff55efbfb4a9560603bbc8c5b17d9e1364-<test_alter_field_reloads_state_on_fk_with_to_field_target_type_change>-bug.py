@skipUnlessDBFeature('supports_foreign_keys')
def test_alter_field_reloads_state_on_fk_with_to_field_target_type_change(self):
    app_label = 'alter_field_reloads_state_on_fk_with_to_field_target_type_change'
    project_state = self.apply_operations(app_label, ProjectState(), operations=[migrations.CreateModel('Rider', fields=[('id', models.AutoField(primary_key=True)), ('code', models.PositiveIntegerField(unique=True))]), migrations.CreateModel('Pony', fields=[('id', models.AutoField(primary_key=True)), ('rider', models.ForeignKey(('%s.Rider' % app_label), models.CASCADE, to_field='code'))])])
    operation = migrations.AlterField('Rider', 'code', models.CharField(max_length=100, unique=True))
    self.apply_operations(app_label, project_state, operations=[operation])