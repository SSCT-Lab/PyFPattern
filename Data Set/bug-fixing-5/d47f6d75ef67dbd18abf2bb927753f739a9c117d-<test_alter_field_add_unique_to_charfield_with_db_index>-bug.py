@unittest.skipUnless((connection.vendor == 'postgresql'), 'PostgreSQL specific')
def test_alter_field_add_unique_to_charfield_with_db_index(self):
    with connection.schema_editor() as editor:
        editor.create_model(BookWithoutAuthor)
    self.assertEqual(self.get_constraints_for_column(BookWithoutAuthor, 'title'), ['schema_book_d5d3db17', 'schema_book_title_2dfb2dff_like'])
    old_field = BookWithoutAuthor._meta.get_field('title')
    new_field = CharField(max_length=100, db_index=True, unique=True)
    new_field.set_attributes_from_name('title')
    with connection.schema_editor() as editor:
        editor.alter_field(BookWithoutAuthor, old_field, new_field, strict=True)
    self.assertEqual(self.get_constraints_for_column(BookWithoutAuthor, 'title'), ['schema_book_d5d3db17', 'schema_book_title_2dfb2dff_like', 'schema_book_title_2dfb2dff_uniq'])
    old_field = BookWithoutAuthor._meta.get_field('title')
    new_field = CharField(max_length=100, db_index=True)
    new_field.set_attributes_from_name('title')
    with connection.schema_editor() as editor:
        editor.alter_field(BookWithoutAuthor, old_field, new_field, strict=True)
    self.assertEqual(self.get_constraints_for_column(BookWithoutAuthor, 'title'), ['schema_book_d5d3db17', 'schema_book_title_2dfb2dff_like', 'schema_book_title_2dfb2dff_uniq'])