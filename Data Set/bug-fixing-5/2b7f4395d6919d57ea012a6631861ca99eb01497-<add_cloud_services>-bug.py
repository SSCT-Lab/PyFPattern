def add_cloud_services(self):
    'Makes an Azure API call to get the list of cloud services.'
    try:
        for cloud_service in self.sms.list_hosted_services():
            self.add_deployments(cloud_service)
    except WindowsAzureError as e:
        print("Looks like Azure's API is down:")
        print('')
        print(e)
        sys.exit(1)