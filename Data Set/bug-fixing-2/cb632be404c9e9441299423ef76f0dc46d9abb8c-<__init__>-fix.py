

@apply_defaults
def __init__(self, sql, druid_datasource, ts_dim, metric_spec=None, hive_cli_conn_id='hive_cli_default', druid_ingest_conn_id='druid_ingest_default', metastore_conn_id='metastore_default', hadoop_dependency_coordinates=None, intervals=None, num_shards=(- 1), target_partition_size=(- 1), query_granularity='NONE', segment_granularity='DAY', hive_tblproperties=None, job_properties=None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.sql = sql
    self.druid_datasource = druid_datasource
    self.ts_dim = ts_dim
    self.intervals = (intervals or ['{{ ds }}/{{ tomorrow_ds }}'])
    self.num_shards = num_shards
    self.target_partition_size = target_partition_size
    self.query_granularity = query_granularity
    self.segment_granularity = segment_granularity
    self.metric_spec = (metric_spec or [{
        'name': 'count',
        'type': 'count',
    }])
    self.hive_cli_conn_id = hive_cli_conn_id
    self.hadoop_dependency_coordinates = hadoop_dependency_coordinates
    self.druid_ingest_conn_id = druid_ingest_conn_id
    self.metastore_conn_id = metastore_conn_id
    self.hive_tblproperties = (hive_tblproperties or {
        
    })
    self.job_properties = job_properties
