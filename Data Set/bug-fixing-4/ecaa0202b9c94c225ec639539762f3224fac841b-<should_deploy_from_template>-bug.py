def should_deploy_from_template(self):
    return (('template' in self.params) and (self.params['template'] is not None))