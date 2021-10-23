def handle(self, request, provider_id):
    pipeline = None
    for pipeline_cls in PIPELINE_CLASSES:
        pipeline = pipeline_cls.get_for_request(request=request)
        if pipeline:
            break
    if ((provider_id in FORWARD_INSTALL_FOR) and (request.GET.get('setup_action') == 'install')):
        installation_id = request.GET.get('installation_id')
        return self.redirect(reverse('integration-installation', args=[installation_id]))
    if ((pipeline is None) or (not pipeline.is_valid())):
        messages.add_message(request, messages.ERROR, _('Invalid request.'))
        return self.redirect('/')
    return pipeline.current_step()