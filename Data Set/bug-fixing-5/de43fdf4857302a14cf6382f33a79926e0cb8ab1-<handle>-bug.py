def handle(self, request, provider_id):
    pipeline = IntegrationPipeline.get_for_request(request=request)
    if (not pipeline):
        logging.error('integration.setup-error')
        return self.redirect('/')
    try:
        return pipeline.current_step()
    except Exception:
        logging.exception('integration.setup-error')
        return pipeline.error('an internal error occurred')