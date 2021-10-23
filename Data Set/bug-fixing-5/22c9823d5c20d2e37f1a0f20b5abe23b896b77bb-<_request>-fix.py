def _request(self, method, path, **kwargs):
    self._ensure_open()
    url = urljoin(self.url, path)
    kwargs.setdefault('headers', {
        
    })['x-sentry-project-id'] = self.project_id
    kwargs.setdefault('headers', {
        
    })['x-sentry-event-id'] = self.event_id
    attempts = 0
    wait = 0.5
    while True:
        try:
            response = self.session.request(method, url, **kwargs)
            metrics.incr('events.symbolicator.status_code', tags={
                'status_code': response.status_code,
                'project_id': self.project_id,
            })
            if ((method.lower() == 'get') and path.startswith('requests/') and (response.status_code == 404)):
                return None
            if (response.status_code in (502, 503)):
                raise ServiceUnavailable()
            if response.ok:
                json = response.json()
            else:
                json = {
                    'status': 'failed',
                    'message': 'internal server error',
                }
            return json
        except (IOError, RequestException):
            attempts += 1
            if (attempts > MAX_ATTEMPTS):
                logger.error('Failed to contact symbolicator', exc_info=True)
                raise
            time.sleep(wait)
            wait *= 2.0