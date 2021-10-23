def get(self, request, user, notification_type):
    if (notification_type not in KEY_MAP):
        return Response({
            'detail': ('Unknown notification type: %s.' % notification_type),
        }, status=status.HTTP_404_NOT_FOUND)
    notifications = UserNotificationsSerializer()
    serialized = serialize(user, request.user, notifications, notification_option_key=KEY_MAP[notification_type]['key'])
    return Response(serialized)