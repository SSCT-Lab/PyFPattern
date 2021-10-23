def add_deployments(self, cloud_service):
    'Makes an Azure API call to get the list of virtual machines\n        associated with a cloud service.\n        '
    try:
        for deployment in self.sms.get_hosted_service_properties(cloud_service.service_name, embed_detail=True).deployments.deployments:
            self.add_deployment(cloud_service, deployment)
    except WindowsAzureError as e:
        print("Looks like Azure's API is down:")
        print('')
        print(e)
        sys.exit(1)