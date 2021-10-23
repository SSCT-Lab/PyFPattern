

def get_ami_info(image):
    return dict(image_id=image.id, state=image.state, architecture=image.architecture, block_device_mapping=get_block_device_mapping(image), creationDate=image.creationDate, description=image.description, hypervisor=image.hypervisor, is_public=image.is_public, location=image.location, ownerId=image.ownerId, root_device_name=image.root_device_name, root_device_type=image.root_device_type, tags=image.tags, virtualization_type=image.virtualization_type)
