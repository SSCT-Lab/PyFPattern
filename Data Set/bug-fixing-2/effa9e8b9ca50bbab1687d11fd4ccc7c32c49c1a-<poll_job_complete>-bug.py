

def poll_job_complete(self, job_id):
    jobs = self.service.jobs()
    try:
        if self.location:
            job = jobs.get(projectId=self.project_id, jobId=job_id, location=self.location).execute()
        else:
            job = jobs.get(projectId=self.project_id, jobId=job_id).execute()
        if (job['status']['state'] == 'DONE'):
            return True
    except HttpError as err:
        if (err.resp.status in [500, 503]):
            self.log.info('%s: Retryable error while polling job with id %s', err.resp.status, job_id)
        else:
            raise Exception('BigQuery job status check failed. Final error was: %s', err.resp.status)
    return False
