def get_job_status(self):
    try:
        check_class = ET.fromstring(self.get_current_config()).tag
        response = self.server.get_job_info(self.name)
        if self.job_class_excluded(check_class):
            return self.EXCL_STATE
        else:
            return response['color'].encode('utf-8')
    except Exception as e:
        self.module.fail_json(msg=('Unable to fetch job information, %s' % to_native(e)), exception=traceback.format_exc())