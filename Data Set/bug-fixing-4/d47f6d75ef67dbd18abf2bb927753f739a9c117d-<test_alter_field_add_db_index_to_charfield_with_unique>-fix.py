@unittest.skipUnless((connection.vendor == 'postgresql'), 'PostgreSQL specific')
def test_alter_field_add_db_index_to_charfield_with_unique(self):
    with connection.schema_editor() as editor:
        editor.create_model(Tag)
    self.assertEqual(self.get_constraints_for_column(Tag, 'slug'), ['schema_tag_slug_2c418ba3_like', 'schema_tag_slug_key'])
    old_field = Tag._meta.get_field('slug')
    new_field = SlugField(db_index=True, unique=True)
    new_field.set_attributes_from_name('slug')
    with connection.schema_editor() as editor:
        editor.alter_field(Tag, old_field, new_field, strict=True)
    self.assertEqual(self.get_constraints_for_column(Tag, 'slug'), ['schema_tag_slug_2c418ba3_like', 'schema_tag_slug_key'])
    new_field2 = SlugField(unique=True)
    new_field2.set_attributes_from_name('slug')
    with connection.schema_editor() as editor:
        editor.alter_field(Tag, new_field, new_field2, strict=True)
    self.assertEqual(self.get_constraints_for_column(Tag, 'slug'), ['schema_tag_slug_2c418ba3_like', 'schema_tag_slug_key'])