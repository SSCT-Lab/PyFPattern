

def handle(self, request, provider_id):
    pipeline = IntegrationPipeline.get_for_request(request=request)
    if (not pipeline):
        logging.error('integration.setup-error')
        return self.redirect('/')
    return pipeline.current_step()
