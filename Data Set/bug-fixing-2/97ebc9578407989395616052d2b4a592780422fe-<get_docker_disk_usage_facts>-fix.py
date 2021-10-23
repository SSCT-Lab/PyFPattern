

def get_docker_disk_usage_facts(self):
    try:
        if self.verbose_output:
            return self.client.df()
        else:
            return dict(LayersSize=self.client.df()['LayersSize'])
    except APIError as exc:
        self.client.fail(('Error inspecting docker host: %s' % to_native(exc)))
