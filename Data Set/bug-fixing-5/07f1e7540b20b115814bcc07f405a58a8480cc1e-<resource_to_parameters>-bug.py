def resource_to_parameters(self, resource):
    ' Converts a resource definition to module parameters '
    parameters = {
        
    }
    for (key, value) in resource.items():
        if (key in ('apiVersion', 'kind', 'status')):
            continue
        elif ((key == 'metadata') and isinstance(value, dict)):
            for (meta_key, meta_value) in value.items():
                if (meta_key in ('name', 'namespace', 'labels', 'annotations')):
                    parameters[meta_key] = meta_value
        elif ((key in self.helper.argspec) and (value is not None)):
            parameters[key] = value
        elif isinstance(value, dict):
            self._add_parameter(value, [key], parameters)
    self.helper.log('Request to parameters: {}'.format(json.dumps(parameters)))
    return parameters