

def cmd_build(self):
    result = dict(changed=False, actions=[])
    if (not self.check_mode):
        for service in self.project.get_services(self.services, include_deps=False):
            if service.can_be_built():
                self.log(('Building image for service %s' % service.name))
                old_image_id = ''
                try:
                    image = service.image()
                    if (image and image.get('Id')):
                        old_image_id = image['Id']
                except NoSuchImageError:
                    pass
                except Exception as exc:
                    self.client.fail(('Error: service image lookup failed - %s' % str(exc)))
                try:
                    new_image_id = service.build(pull=self.pull, no_cache=self.nocache)
                except Exception as exc:
                    self.client.fail(('Error: build failed with %s' % str(exc)))
                if (new_image_id not in old_image_id):
                    result['changed'] = True
                    result['actions'].append(dict(service=service.name, built_image=dict(name=service.image_name, id=new_image_id)))
    return result
