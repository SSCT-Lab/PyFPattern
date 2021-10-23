def put(self, request, project, plugin_id):
    plugin = self._get_plugin(plugin_id)
    config = [serialize_field(project, plugin, c) for c in plugin.get_config(project=project, user=request.user)]
    cleaned = {
        
    }
    errors = {
        
    }
    for field in config:
        key = field['name']
        value = request.DATA.get(key)
        if (field.get('required') and (not value)):
            errors[key] = ERR_FIELD_REQUIRED
        try:
            value = plugin.validate_config_field(project=project, name=key, value=value, actor=request.user)
        except (forms.ValidationError, serializers.ValidationError, PluginError) as e:
            errors[key] = e.message
        if (not errors.get(key)):
            cleaned[key] = value
    if (not errors):
        try:
            cleaned = plugin.validate_config(project=project, config=cleaned, actor=request.user)
        except PluginError as e:
            errors['__all__'] = e.message
    if errors:
        return Response({
            'errors': errors,
        }, status=400)
    for (key, value) in six.iteritems(cleaned):
        if (value is None):
            plugin.unset_option(project=project, key=key)
        else:
            plugin.set_option(project=project, key=key, value=value)
    context = serialize(plugin, request.user, PluginWithConfigSerializer(project))
    plugin_enabled.send(plugin=plugin, project=project, user=request.user, sender=self)
    return Response(context)