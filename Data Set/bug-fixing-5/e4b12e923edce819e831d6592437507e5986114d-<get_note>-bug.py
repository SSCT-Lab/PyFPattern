def get_note(self):
    if (self.event == AuditLogEntryEvent.MEMBER_INVITE):
        return ('invited member %s' % (self.data['email'],))
    elif (self.event == AuditLogEntryEvent.MEMBER_ADD):
        if (self.target_user == self.actor):
            return 'joined the organization'
        return ('added member %s' % (self.target_user.get_display_name(),))
    elif (self.event == AuditLogEntryEvent.MEMBER_ACCEPT):
        return 'accepted the membership invite'
    elif (self.event == AuditLogEntryEvent.MEMBER_REMOVE):
        if (self.target_user == self.actor):
            return 'left the organization'
        return ('removed member %s' % ((self.data.get('email') or self.target_user.get_display_name()),))
    elif (self.event == AuditLogEntryEvent.MEMBER_EDIT):
        return ('edited member %s (role: %s, teams: %s)' % ((self.data.get('email') or self.target_user.get_display_name()), (self.data.get('role') or 'N/A'), (', '.join((six.text_type(x) for x in self.data.get('team_slugs', []))) or 'N/A')))
    elif (self.event == AuditLogEntryEvent.MEMBER_JOIN_TEAM):
        if (self.target_user == self.actor):
            return ('joined team %s' % (self.data['team_slug'],))
        return ('added %s to team %s' % ((self.data.get('email') or self.target_user.get_display_name()), self.data['team_slug']))
    elif (self.event == AuditLogEntryEvent.MEMBER_LEAVE_TEAM):
        if (self.target_user == self.actor):
            return ('left team %s' % (self.data['team_slug'],))
        return ('removed %s from team %s' % ((self.data.get('email') or self.target_user.get_display_name()), self.data['team_slug']))
    elif (self.event == AuditLogEntryEvent.MEMBER_PENDING):
        return ('required member %s to setup 2FA' % ((self.data.get('email') or self.target_user.get_display_name()),))
    elif (self.event == AuditLogEntryEvent.ORG_ADD):
        return 'created the organization'
    elif (self.event == AuditLogEntryEvent.ORG_EDIT):
        return ('edited the organization setting: ' + ', '.join(('{} {}'.format(k, v) for (k, v) in self.data.items())))
    elif (self.event == AuditLogEntryEvent.ORG_REMOVE):
        return 'removed the organization'
    elif (self.event == AuditLogEntryEvent.ORG_RESTORE):
        return 'restored the organization'
    elif (self.event == AuditLogEntryEvent.TEAM_ADD):
        return ('created team %s' % (self.data['slug'],))
    elif (self.event == AuditLogEntryEvent.TEAM_EDIT):
        return ('edited team %s' % (self.data['slug'],))
    elif (self.event == AuditLogEntryEvent.TEAM_REMOVE):
        return ('removed team %s' % (self.data['slug'],))
    elif (self.event == AuditLogEntryEvent.PROJECT_ADD):
        return ('created project %s' % (self.data['slug'],))
    elif (self.event == AuditLogEntryEvent.PROJECT_EDIT):
        return ('edited project settings ' + ' '.join([(' in %s to %s' % (key, value)) for (key, value) in six.iteritems(self.data)]))
    elif (self.event == AuditLogEntryEvent.PROJECT_REMOVE):
        return ('removed project %s' % (self.data['slug'],))
    elif (self.event == AuditLogEntryEvent.PROJECT_REQUEST_TRANSFER):
        return ('requested to transfer project %s' % (self.data['slug'],))
    elif (self.event == AuditLogEntryEvent.PROJECT_ACCEPT_TRANSFER):
        return ('accepted transfer of project %s' % (self.data['slug'],))
    elif (self.event == AuditLogEntryEvent.PROJECT_ENABLE):
        if isinstance(self.data['state'], six.string_types):
            return ('enabled project filter %s' % (self.data['state'],))
        return ('enabled project filter %s' % (', '.join(self.data['state']),))
    elif (self.event == AuditLogEntryEvent.PROJECT_DISABLE):
        if isinstance(self.data['state'], six.string_types):
            return ('disabled project filter %s' % (self.data['state'],))
        return ('disabled project filter %s' % (', '.join(self.data['state']),))
    elif (self.event == AuditLogEntryEvent.TAGKEY_REMOVE):
        return ('removed tags matching %s = *' % (self.data['key'],))
    elif (self.event == AuditLogEntryEvent.PROJECTKEY_ADD):
        return ('added project key %s' % (self.data['public_key'],))
    elif (self.event == AuditLogEntryEvent.PROJECTKEY_EDIT):
        return ('edited project key %s' % (self.data['public_key'],))
    elif (self.event == AuditLogEntryEvent.PROJECTKEY_REMOVE):
        return ('removed project key %s' % (self.data['public_key'],))
    elif (self.event == AuditLogEntryEvent.PROJECTKEY_ENABLE):
        return ('enabled project key %s' % (self.data['public_key'],))
    elif (self.event == AuditLogEntryEvent.PROJECTKEY_DISABLE):
        return ('disabled project key %s' % (self.data['public_key'],))
    elif (self.event == AuditLogEntryEvent.SSO_ENABLE):
        return ('enabled sso (%s)' % (self.data['provider'],))
    elif (self.event == AuditLogEntryEvent.SSO_DISABLE):
        return ('disabled sso (%s)' % (self.data['provider'],))
    elif (self.event == AuditLogEntryEvent.SSO_EDIT):
        return ('edited sso settings: ' + ', '.join(('{} {}'.format(k, v) for (k, v) in self.data.items())))
    elif (self.event == AuditLogEntryEvent.SSO_IDENTITY_LINK):
        return 'linked their account to a new identity'
    elif (self.event == AuditLogEntryEvent.APIKEY_ADD):
        return ('added api key %s' % (self.data['label'],))
    elif (self.event == AuditLogEntryEvent.APIKEY_EDIT):
        return ('edited api key %s' % (self.data['label'],))
    elif (self.event == AuditLogEntryEvent.APIKEY_REMOVE):
        return ('removed api key %s' % (self.data['label'],))
    elif (self.event == AuditLogEntryEvent.RULE_ADD):
        return ('added rule "%s"' % (self.data['label'],))
    elif (self.event == AuditLogEntryEvent.RULE_EDIT):
        return ('edited rule "%s"' % (self.data['label'],))
    elif (self.event == AuditLogEntryEvent.RULE_REMOVE):
        return ('removed rule "%s"' % (self.data['label'],))
    elif (self.event == AuditLogEntryEvent.SET_ONDEMAND):
        if (self.data['ondemand'] == (- 1)):
            return 'changed on-demand spend to unlimited'
        return ('changed on-demand max spend to $%d' % ((self.data['ondemand'] / 100),))
    elif (self.event == AuditLogEntryEvent.TRIAL_STARTED):
        return 'started trial'
    elif (self.event == AuditLogEntryEvent.PLAN_CHANGED):
        return ('changed plan to %s' % (self.data['plan_name'],))
    elif (self.event == AuditLogEntryEvent.PLAN_CANCELLED):
        return 'cancelled plan'
    elif (self.event == AuditLogEntryEvent.SERVICEHOOK_ADD):
        return ('added a service hook for "%s"' % (truncatechars(self.data['url'], 64),))
    elif (self.event == AuditLogEntryEvent.SERVICEHOOK_EDIT):
        return ('edited the service hook for "%s"' % (truncatechars(self.data['url'], 64),))
    elif (self.event == AuditLogEntryEvent.SERVICEHOOK_REMOVE):
        return ('removed the service hook for "%s"' % (truncatechars(self.data['url'], 64),))
    elif (self.event == AuditLogEntryEvent.SERVICEHOOK_ENABLE):
        return ('enabled theservice hook for "%s"' % (truncatechars(self.data['url'], 64),))
    elif (self.event == AuditLogEntryEvent.SERVICEHOOK_DISABLE):
        return ('disabled the service hook for "%s"' % (truncatechars(self.data['url'], 64),))
    elif (self.event == AuditLogEntryEvent.INTEGRATION_ADD):
        return ('enabled integration %s for project %s' % (self.data['integration'], self.data['project']))
    elif (self.event == AuditLogEntryEvent.INTEGRATION_EDIT):
        return ('edited integration %s for project %s' % (self.data['integration'], self.data['project']))
    elif (self.event == AuditLogEntryEvent.INTEGRATION_REMOVE):
        return ('disabled integration %s from project %s' % (self.data['integration'], self.data['project']))
    elif (self.event == AuditLogEntryEvent.SENTRY_APP_ADD):
        return ('created sentry app %s' % self.data['sentry_app'])
    elif (self.event == AuditLogEntryEvent.SENTRY_APP_REMOVE):
        return ('removed sentry app %s' % self.data['sentry_app'])
    elif (self.event == AuditLogEntryEvent.SENTRY_APP_INSTALL):
        return ('installed sentry app %s' % self.data['sentry_app'])
    elif (self.event == AuditLogEntryEvent.SENTRY_APP_UNINSTALL):
        return ('uninstalled sentry app %s' % self.data['sentry_app'])
    return ''