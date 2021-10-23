

def get_validated_data(self, data, user):
    try:
        data = unsign(force_str(data))
    except SignatureExpired:
        raise InvalidPayload('Project transfer link has expired.')
    except BadSignature:
        raise InvalidPayload('Could not approve transfer, please make sure link is valid.')
    if (data['user_id'] != user.id):
        raise InvalidPayload('Invalid permissions')
    try:
        project = Project.objects.get(id=data['project_id'], organization_id=data['from_organization_id'])
    except Project.DoesNotExist:
        raise InvalidPayload('Project no longer exists')
    return (data, project)
