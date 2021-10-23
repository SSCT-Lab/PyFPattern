

def test_unsupported_backend(self):
    msg = 'This backend does not support window expressions.'
    with mock.patch.object(connection.features, 'supports_over_clause', False):
        with self.assertRaisesMessage(NotSupportedError, msg):
            Employee.objects.annotate(dense_rank=Window(expression=DenseRank())).get()
