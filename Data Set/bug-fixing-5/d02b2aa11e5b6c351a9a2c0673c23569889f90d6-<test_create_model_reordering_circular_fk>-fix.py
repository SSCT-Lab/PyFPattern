def test_create_model_reordering_circular_fk(self):
    "\n        CreateModel reordering behavior doesn't result in an infinite loop if\n        there are FKs in both directions.\n        "
    self.assertOptimizesTo([migrations.CreateModel('Bar', [('url', models.TextField())]), migrations.CreateModel('Foo', [('name', models.CharField(max_length=255))]), migrations.AddField('Bar', 'foo_fk', models.ForeignKey('migrations.Foo', models.CASCADE)), migrations.AddField('Foo', 'bar_fk', models.ForeignKey('migrations.Bar', models.CASCADE))], [migrations.CreateModel('Foo', [('name', models.CharField(max_length=255))]), migrations.CreateModel('Bar', [('url', models.TextField()), ('foo_fk', models.ForeignKey('migrations.Foo', models.CASCADE))]), migrations.AddField('Foo', 'bar_fk', models.ForeignKey('migrations.Bar', models.CASCADE))])