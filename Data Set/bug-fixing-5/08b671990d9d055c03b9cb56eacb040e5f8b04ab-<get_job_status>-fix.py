def get_job_status(self):
    try:
        response = self.server.get_job_info(self.name)
        if self.job_class_excluded(response):
            return self.EXCL_STATE
        else:
            return response['color'].encode('utf-8')
    except Exception:
        e = get_exception()
        self.module.fail_json(msg=('Unable to fetch job information, %s' % str(e)))