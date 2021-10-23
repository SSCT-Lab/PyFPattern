def __init__(self, api_version: str='v3', gcp_conn_id: str='google_cloud_default', delegate_to: str=None) -> None:
    super().__init__(gcp_conn_id, delegate_to)
    self.api_version = api_version