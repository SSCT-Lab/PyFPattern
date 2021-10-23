

@GoogleCloudBaseHook.fallback_to_default_project_id
def create_cluster(self, cluster: Union[(Dict, Cluster)], project_id: Optional[str]=None, retry: Retry=DEFAULT, timeout: float=DEFAULT) -> str:
    '\n        Creates a cluster, consisting of the specified number and type of Google Compute\n        Engine instances.\n\n        :param cluster: A Cluster protobuf or dict. If dict is provided, it must\n            be of the same form as the protobuf message\n            :class:`google.cloud.container_v1.types.Cluster`\n        :type cluster: dict or google.cloud.container_v1.types.Cluster\n        :param project_id: Google Cloud Platform project ID\n        :type project_id: str\n        :param retry: A retry object (``google.api_core.retry.Retry``) used to\n            retry requests.\n            If None is specified, requests will not be retried.\n        :type retry: google.api_core.retry.Retry\n        :param timeout: The amount of time, in seconds, to wait for the request to\n            complete. Note that if retry is specified, the timeout applies to each\n            individual attempt.\n        :type timeout: float\n        :return: The full url to the new, or existing, cluster\n        :raises:\n            ParseError: On JSON parsing problems when trying to convert dict\n            AirflowException: cluster is not dict type nor Cluster proto type\n        '
    if isinstance(cluster, dict):
        cluster_proto = Cluster()
        cluster = ParseDict(cluster, cluster_proto)
    elif (not isinstance(cluster, Cluster)):
        raise AirflowException('cluster is not instance of Cluster proto or python dict')
    self._append_label(cluster, 'airflow-version', ('v' + version.version))
    self.log.info('Creating (project_id=%s, zone=%s, cluster_name=%s)', project_id, self.location, cluster.name)
    try:
        resource = self.get_conn().create_cluster(project_id=project_id, zone=self.location, cluster=cluster, retry=retry, timeout=timeout)
        resource = self.wait_for_operation(resource)
        return resource.target_link
    except AlreadyExists as error:
        self.log.info('Assuming Success: %s', error.message)
        return self.get_cluster(name=cluster.name).self_link
