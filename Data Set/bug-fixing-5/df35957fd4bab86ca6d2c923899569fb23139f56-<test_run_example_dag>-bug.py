@provide_gcp_context(GCP_GCS_KEY)
def test_run_example_dag(self):
    self.run_dag('example_sftp_to_gcs', GCP_DAG_FOLDER)