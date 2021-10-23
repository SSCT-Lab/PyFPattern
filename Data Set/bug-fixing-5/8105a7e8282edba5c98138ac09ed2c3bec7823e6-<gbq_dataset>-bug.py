@pytest.fixture()
def gbq_dataset(self):
    _skip_if_no_project_id()
    _skip_if_no_private_key_path()
    dataset_id = 'pydata_pandas_bq_testing_py31'
    self.client = _get_client()
    self.dataset = self.client.dataset(dataset_id)
    try:
        self.client.delete_dataset(self.dataset, delete_contents=True)
    except api_exceptions.NotFound:
        pass
    self.client.create_dataset(bigquery.Dataset(self.dataset))
    table_name = ''.join(random.choices(string.ascii_lowercase, k=10))
    destination_table = f'{dataset_id}.{table_name}'
    (yield destination_table)
    self.client.delete_dataset(self.dataset, delete_contents=True)