

def get_hook(self):
    if (self.conn_type == 'mysql'):
        from airflow.hooks.mysql_hook import MySqlHook
        return MySqlHook(mysql_conn_id=self.conn_id)
    elif (self.conn_type == 'google_cloud_platform'):
        from airflow.gcp.hooks.bigquery import BigQueryHook
        return BigQueryHook(bigquery_conn_id=self.conn_id)
    elif (self.conn_type == 'postgres'):
        from airflow.hooks.postgres_hook import PostgresHook
        return PostgresHook(postgres_conn_id=self.conn_id)
    elif (self.conn_type == 'pig_cli'):
        from airflow.hooks.pig_hook import PigCliHook
        return PigCliHook(pig_conn_id=self.conn_id)
    elif (self.conn_type == 'hive_cli'):
        from airflow.hooks.hive_hooks import HiveCliHook
        return HiveCliHook(hive_cli_conn_id=self.conn_id)
    elif (self.conn_type == 'presto'):
        from airflow.hooks.presto_hook import PrestoHook
        return PrestoHook(presto_conn_id=self.conn_id)
    elif (self.conn_type == 'hiveserver2'):
        from airflow.hooks.hive_hooks import HiveServer2Hook
        return HiveServer2Hook(hiveserver2_conn_id=self.conn_id)
    elif (self.conn_type == 'sqlite'):
        from airflow.hooks.sqlite_hook import SqliteHook
        return SqliteHook(sqlite_conn_id=self.conn_id)
    elif (self.conn_type == 'jdbc'):
        from airflow.hooks.jdbc_hook import JdbcHook
        return JdbcHook(jdbc_conn_id=self.conn_id)
    elif (self.conn_type == 'mssql'):
        from airflow.hooks.mssql_hook import MsSqlHook
        return MsSqlHook(mssql_conn_id=self.conn_id)
    elif (self.conn_type == 'oracle'):
        from airflow.hooks.oracle_hook import OracleHook
        return OracleHook(oracle_conn_id=self.conn_id)
    elif (self.conn_type == 'vertica'):
        from airflow.contrib.hooks.vertica_hook import VerticaHook
        return VerticaHook(vertica_conn_id=self.conn_id)
    elif (self.conn_type == 'cloudant'):
        from airflow.contrib.hooks.cloudant_hook import CloudantHook
        return CloudantHook(cloudant_conn_id=self.conn_id)
    elif (self.conn_type == 'jira'):
        from airflow.contrib.hooks.jira_hook import JiraHook
        return JiraHook(jira_conn_id=self.conn_id)
    elif (self.conn_type == 'redis'):
        from airflow.contrib.hooks.redis_hook import RedisHook
        return RedisHook(redis_conn_id=self.conn_id)
    elif (self.conn_type == 'wasb'):
        from airflow.contrib.hooks.wasb_hook import WasbHook
        return WasbHook(wasb_conn_id=self.conn_id)
    elif (self.conn_type == 'docker'):
        from airflow.hooks.docker_hook import DockerHook
        return DockerHook(docker_conn_id=self.conn_id)
    elif (self.conn_type == 'azure_data_lake'):
        from airflow.contrib.hooks.azure_data_lake_hook import AzureDataLakeHook
        return AzureDataLakeHook(azure_data_lake_conn_id=self.conn_id)
    elif (self.conn_type == 'azure_cosmos'):
        from airflow.contrib.hooks.azure_cosmos_hook import AzureCosmosDBHook
        return AzureCosmosDBHook(azure_cosmos_conn_id=self.conn_id)
    elif (self.conn_type == 'cassandra'):
        from airflow.contrib.hooks.cassandra_hook import CassandraHook
        return CassandraHook(cassandra_conn_id=self.conn_id)
    elif (self.conn_type == 'mongo'):
        from airflow.contrib.hooks.mongo_hook import MongoHook
        return MongoHook(conn_id=self.conn_id)
    elif (self.conn_type == 'gcpcloudsql'):
        from airflow.gcp.hooks.cloud_sql import CloudSqlDatabaseHook
        return CloudSqlDatabaseHook(gcp_cloudsql_conn_id=self.conn_id)
    elif (self.conn_type == 'grpc'):
        from airflow.contrib.hooks.grpc_hook import GrpcHook
        return GrpcHook(grpc_conn_id=self.conn_id)
    raise AirflowException('Unknown hook type {}'.format(self.conn_type))
