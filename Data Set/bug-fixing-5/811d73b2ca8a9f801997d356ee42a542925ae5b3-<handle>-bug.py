def handle(self, request, organization, provider_id):
    pipeline = IntegrationPipeline(request=request, organization=organization, provider_key=provider_id)
    pipeline.initialize()
    return pipeline.current_step()