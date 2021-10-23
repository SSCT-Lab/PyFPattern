@apply_defaults
def __init__(self, cql, bucket, filename, schema_filename=None, approx_max_file_size_bytes=1900000000, cassandra_conn_id='cassandra_default', google_cloud_storage_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
    '\n        :param cql: The CQL to execute on the Cassandra table.\n        :type cql: str\n        :param bucket: The bucket to upload to.\n        :type bucket: str\n        :param filename: The filename to use as the object name when uploading\n            to Google cloud storage. A {} should be specified in the filename\n            to allow the operator to inject file numbers in cases where the\n            file is split due to size.\n        :type filename: str\n        :param schema_filename: If set, the filename to use as the object name\n            when uploading a .json file containing the BigQuery schema fields\n            for the table that was dumped from MySQL.\n        :type schema_filename: str\n        :param approx_max_file_size_bytes: This operator supports the ability\n            to split large table dumps into multiple files (see notes in the\n            filenamed param docs above). Google cloud storage allows for files\n            to be a maximum of 4GB. This param allows developers to specify the\n            file size of the splits.\n        :type approx_max_file_size_bytes: long\n        :param cassandra_conn_id: Reference to a specific Cassandra hook.\n        :type cassandra_conn_id: str\n        :param google_cloud_storage_conn_id: Reference to a specific Google\n            cloud storage hook.\n        :type google_cloud_storage_conn_id: str\n        :param delegate_to: The account to impersonate, if any. For this to\n            work, the service account making the request must have domain-wide\n            delegation enabled.\n        :type delegate_to: str\n        '
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