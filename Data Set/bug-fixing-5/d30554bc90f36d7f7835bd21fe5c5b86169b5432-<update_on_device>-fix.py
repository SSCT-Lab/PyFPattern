def update_on_device(self):
    params = self.changes.api_params()
    resource = self.client.api.tm.sys.httpd.load()
    try:
        resource.modify(**params)
        return True
    except ConnectionError as ex:
        if (('Connection aborted' in str(ex)) and ('redirectHttpToHttps' in params)):
            time.sleep(2)
            return True
        raise F5ModuleError(str(ex))