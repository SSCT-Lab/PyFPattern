def get_job_status(self):
    try:
        response = self.server.get_job_info(self.name)
        if ('color' not in response):
            return self.EXCL_STATE
        else:
            return response['color'].encode('utf-8')
    except Exception as e:
        self.module.fail_json(msg=('Unable to fetch job information, %s' % to_native(e)), exception=traceback.format_exc())