@pytest.fixture()
def gbq_dataset(self):
    _skip_if_no_project_id()
    _skip_if_no_private_key_path()
    dataset_id = ('pydata_pandas_bq_testing_' + generate_rand_str())
    self.client = _get_client()
    self.dataset = self.client.dataset(dataset_id)
    self.client.create_dataset(bigquery.Dataset(self.dataset))
    table_name = generate_rand_str()
    destination_table = f'{dataset_id}.{table_name}'
    (yield destination_table)
    self.client.delete_dataset(self.dataset, delete_contents=True)