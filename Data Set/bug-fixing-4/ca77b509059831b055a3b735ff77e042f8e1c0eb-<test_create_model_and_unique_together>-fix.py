def test_create_model_and_unique_together(self):
    author = ModelState('otherapp', 'Author', [('id', models.AutoField(primary_key=True)), ('name', models.CharField(max_length=200))])
    book_with_author = ModelState('otherapp', 'Book', [('id', models.AutoField(primary_key=True)), ('author', models.ForeignKey('otherapp.Author', models.CASCADE)), ('title', models.CharField(max_length=200))], {
        'index_together': {('title', 'author')},
        'unique_together': {('title', 'author')},
    })
    changes = self.get_changes([self.book_with_no_author], [author, book_with_author])
    self.assertEqual(len(changes['otherapp']), 1)
    migration = changes['otherapp'][0]
    self.assertEqual(len(migration.operations), 4)
    self.assertOperationTypes(changes, 'otherapp', 0, ['CreateModel', 'AddField', 'AlterUniqueTogether', 'AlterIndexTogether'])