

def test_large_delete_related(self):
    TEST_SIZE = 2000
    s = S.objects.create(r=R.objects.create())
    for i in range(TEST_SIZE):
        T.objects.create(s=s)
    batch_size = max(connection.ops.bulk_batch_size(['pk'], range(TEST_SIZE)), 1)
    expected_num_queries = ((ceil((TEST_SIZE // batch_size)) + ceil((TEST_SIZE // GET_ITERATOR_CHUNK_SIZE))) + 2)
    self.assertNumQueries(expected_num_queries, s.delete)
    self.assertFalse(S.objects.exists())
    self.assertFalse(T.objects.exists())
