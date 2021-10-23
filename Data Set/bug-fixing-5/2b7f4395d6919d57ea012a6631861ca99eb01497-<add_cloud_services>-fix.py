def add_cloud_services(self):
    'Makes an Azure API call to get the list of cloud services.'
    try:
        for cloud_service in self.sms.list_hosted_services():
            self.add_deployments(cloud_service)
    except Exception as e:
        sys.exit('Error: Failed to access cloud services - {0}'.format(str(e)))