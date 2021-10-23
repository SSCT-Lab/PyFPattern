

@GoogleCloudBaseHook.fallback_to_default_project_id
def get_job(self, location: str, job_id: str, project_id: Optional[str]=None, retry: Optional[Retry]=None, timeout: Optional[float]=None, metadata: Optional[Sequence[Tuple[(str, str)]]]=None) -> Job:
    '\n        Gets the resource representation for a job in a project.\n\n        :param job_id: Id of the Dataproc job\n        :type job_id: str\n        :param project_id: Required. The ID of the Google Cloud Platform project the cluster belongs to.\n        :type project_id: str\n        :param location: Required. The Cloud Dataproc region in which to handle the request.\n        :type location: str\n        :param retry: A retry object used to retry requests. If ``None`` is specified, requests will not be\n            retried.\n        :type retry: google.api_core.retry.Retry\n        :param timeout: The amount of time, in seconds, to wait for the request to complete. Note that if\n            ``retry`` is specified, the timeout applies to each individual attempt.\n        :type timeout: float\n        :param metadata: Additional metadata that is provided to the method.\n        :type metadata: Sequence[Tuple[str, str]]\n        '
    client = self.get_job_client(location=location)
    job = client.get_job(project_id=project_id, region=location, job_id=job_id, retry=retry, timeout=timeout, metadata=metadata)
    return job
