def put(self, request, user, notification_type):
    '\n        Update user notification options\n        ````````````````````````````````\n\n        Updates user\'s notification options on a per project or organization basis.\n        Expected payload is a map/dict whose key is a project or org id and value varies depending on `notification_type`.\n\n        For `alerts`, `workflow`, `email` it expects a key of projectId\n        For `deploy` and `reports` it expects a key of organizationId\n\n        For `alerts`, `workflow`, `deploy`, it expects a value of:\n            - "-1" = for "default" value (i.e. delete the option)\n            - "0"  = disabled\n            - "1"  = enabled\n        For `reports` it is only a boolean.\n        For `email` it is a verified email (string).\n\n        :auth required:\n        :pparam string notification_type:  One of:  alerts, workflow, reports, deploy, email\n        :param map: Expects a map of id -> value (enabled or email)\n        '
    if (notification_type not in KEY_MAP):
        return Response(status=status.HTTP_404_NOT_FOUND)
    key = KEY_MAP[notification_type]
    filter_args = {
        'user': user,
        'key': key['key'],
    }
    if (notification_type == 'reports'):
        (user_option, created) = UserOption.objects.get_or_create(**filter_args)
        value = set((user_option.value or []))
        org_ids = self.get_org_ids(user)
        for (org_id, enabled) in request.data.items():
            org_id = int(org_id)
            enabled = int(enabled)
            if (org_id not in org_ids):
                return Response(status=status.HTTP_403_FORBIDDEN)
            if (enabled and (org_id in value)):
                value.remove(org_id)
            elif (not enabled):
                value.add(org_id)
        user_option.update(value=list(value))
        return Response(status=status.HTTP_204_NO_CONTENT)
    if (notification_type in ['alerts', 'workflow', 'email']):
        update_key = 'project'
        parent_ids = set(self.get_project_ids(user))
    else:
        update_key = 'organization'
        parent_ids = set(self.get_org_ids(user))
    try:
        ids_to_update = set([int(i) for i in request.data.keys()])
    except ValueError:
        return Response({
            'detail': 'Invalid id value provided. Id values should be integers.',
        }, status=status.HTTP_400_BAD_REQUEST)
    if (not ids_to_update.issubset(parent_ids)):
        return Response(status=status.HTTP_403_FORBIDDEN)
    if (notification_type == 'email'):
        emails_to_check = set(request.data.values())
        emails = UserEmail.objects.filter(user=user, email__in=emails_to_check, is_verified=True)
        if (len(emails) != len(emails_to_check)):
            return Response(status=status.HTTP_400_BAD_REQUEST)
    with transaction.atomic():
        for id in request.data:
            val = request.data[id]
            int_val = (int(val) if (notification_type != 'email') else None)
            filter_args[('%s_id' % update_key)] = id
            if (int_val == (- 1)):
                UserOption.objects.filter(**filter_args).delete()
            else:
                (user_option, _) = UserOption.objects.get_or_create(**filter_args)
                user_option.update(value=(int_val if (key['type'] is int) else six.text_type(val)))
        return Response(status=status.HTTP_204_NO_CONTENT)