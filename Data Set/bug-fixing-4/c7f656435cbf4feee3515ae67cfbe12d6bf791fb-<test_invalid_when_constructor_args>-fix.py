def test_invalid_when_constructor_args(self):
    msg = '__init__() takes either a Q object or lookups as keyword arguments'
    with self.assertRaisesMessage(TypeError, msg):
        When(condition=object())
    with self.assertRaisesMessage(TypeError, msg):
        When(condition=Value(1, output_field=models.IntegerField()))
    with self.assertRaisesMessage(TypeError, msg):
        When()