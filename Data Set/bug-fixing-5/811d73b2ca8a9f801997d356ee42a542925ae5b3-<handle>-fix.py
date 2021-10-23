def handle(self, request, organization, provider_id):
    pipeline = IntegrationPipeline(request=request, organization=organization, provider_key=provider_id)
    if (not pipeline.provider.can_add):
        raise Http404
    pipeline.initialize()
    return pipeline.current_step()