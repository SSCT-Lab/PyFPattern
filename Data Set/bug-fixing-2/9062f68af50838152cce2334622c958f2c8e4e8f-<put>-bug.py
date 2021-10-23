

def put(self, request, group, integration_id):
    external_issue_id = request.DATA.get('externalIssue')
    if (not external_issue_id):
        return Response({
            'detail': 'External ID required',
        }, status=400)
    organization_id = group.project.organization_id
    try:
        integration = OrganizationIntegration.objects.filter(integration_id=integration_id, organization_id=organization_id).select_related('integration').get().integration
    except OrganizationIntegration.DoesNotExist:
        return Response(status=404)
    if (not integration.has_feature(IntegrationFeatures.ISSUE_SYNC)):
        return Response({
            'detail': 'This feature is not supported for this integration.',
        }, status=400)
    installation = integration.get_installation()
    try:
        data = installation.get_issue(external_issue_id)
    except IntegrationError as exc:
        return Response({
            'detail': exc.message,
        }, status=400)
    external_issue = ExternalIssue.objects.get_or_create(organization_id=organization_id, integration_id=integration.id, key=external_issue_id, title=data.get('title'), description=data.get('description'))[0]
    try:
        with transaction.atomic():
            GroupLink.objects.create(group_id=group.id, project_id=group.project_id, linked_type=GroupLink.LinkedType.issue, linked_id=external_issue.id, relationship=GroupLink.Relationship.references)
    except IntegrityError:
        return Response({
            'non_field_errors': ['That issue is already linked'],
        }, status=400)
    return Response(status=201)
