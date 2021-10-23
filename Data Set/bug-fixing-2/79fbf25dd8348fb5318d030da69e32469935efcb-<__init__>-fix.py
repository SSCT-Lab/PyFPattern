

@apply_defaults
def __init__(self, cql, bucket, filename, schema_filename=None, approx_max_file_size_bytes=1900000000, cassandra_conn_id='cassandra_default', google_cloud_storage_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
    super(CassandraToGoogleCloudStorageOperator, self).__init__(*args, **kwargs)
    self.cql = cql
    self.bucket = bucket
    self.filename = filename
    self.schema_filename = schema_filename
    self.approx_max_file_size_bytes = approx_max_file_size_bytes
    self.cassandra_conn_id = cassandra_conn_id
    self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
    self.delegate_to = delegate_to
    self.hook = None
