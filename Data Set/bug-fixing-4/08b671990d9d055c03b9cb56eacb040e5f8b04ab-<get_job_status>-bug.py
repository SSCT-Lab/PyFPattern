def get_job_status(self):
    try:
        return self.server.get_job_info(self.name)['color'].encode('utf-8')
    except Exception:
        e = get_exception()
        self.module.fail_json(msg=('Unable to fetch job information, %s' % str(e)))