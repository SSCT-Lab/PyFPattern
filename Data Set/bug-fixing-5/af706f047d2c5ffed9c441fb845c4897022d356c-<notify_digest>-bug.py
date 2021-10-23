def notify_digest(self, project, digest):
    (start, end, counts) = get_digest_metadata(digest)
    if (len(counts) == 1):
        group = six.next(iter(counts))
        record = max(itertools.chain.from_iterable((groups.get(group, []) for groups in six.itervalues(digest))), key=(lambda record: record.timestamp))
        notification = Notification(record.value.event, rules=record.value.rules)
        return self.notify(notification)
    context = {
        'start': start,
        'end': end,
        'project': project,
        'digest': digest,
        'counts': counts,
    }
    subject = self.get_digest_subject(project, counts, start)
    for user_id in self.get_send_to(project):
        self.add_unsubscribe_link(context, user_id, project)
        self._send_mail(subject=subject, template='sentry/emails/digests/body.txt', html_template='sentry/emails/digests/body.html', project=project, reference=project, type='notify.digest', context=context, send_to=[user_id])