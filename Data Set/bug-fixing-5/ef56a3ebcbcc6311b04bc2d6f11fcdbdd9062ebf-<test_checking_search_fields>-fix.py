def test_checking_search_fields(self):
    with patch_search_fields(models.SearchTest, (models.SearchTest.search_fields + [index.SearchField('foo')])):
        expected_errors = [checks.Warning("SearchTest.search_fields contains field 'foo' but it doesn't exist", obj=models.SearchTest)]
        errors = models.SearchTest.check()
        self.assertEqual(errors, expected_errors)