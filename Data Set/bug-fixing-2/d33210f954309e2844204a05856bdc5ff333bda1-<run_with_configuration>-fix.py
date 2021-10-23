

def run_with_configuration(self, configuration):
    "\n        Executes a BigQuery SQL query. See here:\n\n        https://cloud.google.com/bigquery/docs/reference/v2/jobs\n\n        For more details about the configuration parameter.\n\n        :param configuration: The configuration parameter maps directly to\n            BigQuery's configuration field in the job object. See\n            https://cloud.google.com/bigquery/docs/reference/v2/jobs for\n            details.\n        "
    jobs = self.service.jobs()
    job_data = {
        'configuration': configuration,
    }
    query_reply = jobs.insert(projectId=self.project_id, body=job_data).execute()
    self.running_job_id = query_reply['jobReference']['jobId']
    if ('location' in query_reply['jobReference']):
        location = query_reply['jobReference']['location']
    else:
        location = self.location
    keep_polling_job = True
    while keep_polling_job:
        try:
            if location:
                job = jobs.get(projectId=self.project_id, jobId=self.running_job_id, location=location).execute()
            else:
                job = jobs.get(projectId=self.project_id, jobId=self.running_job_id).execute()
            if (job['status']['state'] == 'DONE'):
                keep_polling_job = False
                if ('errorResult' in job['status']):
                    raise Exception('BigQuery job failed. Final error was: {}. The job was: {}'.format(job['status']['errorResult'], job))
            else:
                self.log.info('Waiting for job to complete : %s, %s', self.project_id, self.running_job_id)
                time.sleep(5)
        except HttpError as err:
            if (err.resp.status in [500, 503]):
                self.log.info('%s: Retryable error, waiting for job to complete: %s', err.resp.status, self.running_job_id)
                time.sleep(5)
            else:
                raise Exception('BigQuery job status check failed. Final error was: {}'.format(err.resp.status))
    return self.running_job_id
