@GoogleCloudBaseHook.catch_http_exception
@GoogleCloudBaseHook.fallback_to_default_project_id
def create_bucket(self, bucket_name, resource=None, storage_class='MULTI_REGIONAL', location='US', project_id=None, labels=None):
    "\n        Creates a new bucket. Google Cloud Storage uses a flat namespace, so\n        you can't create a bucket with a name that is already in use.\n\n        .. seealso::\n            For more information, see Bucket Naming Guidelines:\n            https://cloud.google.com/storage/docs/bucketnaming.html#requirements\n\n        :param bucket_name: The name of the bucket.\n        :type bucket_name: str\n        :param resource: An optional dict with parameters for creating the bucket.\n            For information on available parameters, see Cloud Storage API doc:\n            https://cloud.google.com/storage/docs/json_api/v1/buckets/insert\n        :type resource: dict\n        :param storage_class: This defines how objects in the bucket are stored\n            and determines the SLA and the cost of storage. Values include\n\n            - ``MULTI_REGIONAL``\n            - ``REGIONAL``\n            - ``STANDARD``\n            - ``NEARLINE``\n            - ``COLDLINE``.\n\n            If this value is not specified when the bucket is\n            created, it will default to STANDARD.\n        :type storage_class: str\n        :param location: The location of the bucket.\n            Object data for objects in the bucket resides in physical storage\n            within this region. Defaults to US.\n\n            .. seealso::\n                https://developers.google.com/storage/docs/bucket-locations\n\n        :type location: str\n        :param project_id: The ID of the GCP Project.\n        :type project_id: str\n        :param labels: User-provided labels, in key/value pairs.\n        :type labels: dict\n        :return: If successful, it returns the ``id`` of the bucket.\n        "
    self.log.info('Creating Bucket: %s; Location: %s; Storage Class: %s', bucket_name, location, storage_class)
    labels = ({
        
    } or labels)
    labels['airflow-version'] = ('v' + version.replace('.', '-').replace('+', '-'))
    client = self.get_conn()
    bucket = client.bucket(bucket_name=bucket_name)
    bucket_resource = (resource or {
        
    })
    for item in bucket_resource:
        if (item != 'name'):
            bucket._patch_property(name=item, value=resource[item])
    bucket.storage_class = storage_class
    bucket.labels = labels
    bucket.create(project=project_id, location=location)
    return bucket.id