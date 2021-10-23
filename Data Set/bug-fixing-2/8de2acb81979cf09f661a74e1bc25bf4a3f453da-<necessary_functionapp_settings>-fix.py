

def necessary_functionapp_settings(self):
    'Construct the necessary app settings required for an Azure Function App'
    function_app_settings = []
    if (self.container_settings is None):
        for key in ['AzureWebJobsStorage', 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING', 'AzureWebJobsDashboard']:
            function_app_settings.append(NameValuePair(name=key, value=self.storage_connection_string))
        function_app_settings.append(NameValuePair(name='FUNCTIONS_EXTENSION_VERSION', value='~1'))
        function_app_settings.append(NameValuePair(name='WEBSITE_NODE_DEFAULT_VERSION', value='6.5.0'))
        function_app_settings.append(NameValuePair(name='WEBSITE_CONTENTSHARE', value=self.name))
    else:
        function_app_settings.append(NameValuePair(name='FUNCTIONS_EXTENSION_VERSION', value='~2'))
        function_app_settings.append(NameValuePair(name='WEBSITES_ENABLE_APP_SERVICE_STORAGE', value=False))
        function_app_settings.append(NameValuePair(name='AzureWebJobsStorage', value=self.storage_connection_string))
    return function_app_settings
