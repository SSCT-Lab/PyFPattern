def should_deploy_from_template(self):
    return (self.params.get('template') is not None)