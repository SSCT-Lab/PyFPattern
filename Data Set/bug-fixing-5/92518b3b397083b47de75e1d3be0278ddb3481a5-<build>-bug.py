def build(self, to, reply_to=None, cc=None, bcc=None):
    if (self.headers is None):
        headers = {
            
        }
    else:
        headers = self.headers.copy()
    if (options.get('mail.enable-replies') and ('X-Sentry-Reply-To' in headers)):
        reply_to = headers['X-Sentry-Reply-To']
    else:
        reply_to = set((reply_to or ()))
        reply_to.remove(to)
        reply_to = ', '.join(reply_to)
    if reply_to:
        headers.setdefault('Reply-To', reply_to)
    message_id = make_msgid(get_from_email_domain())
    headers.setdefault('Message-Id', message_id)
    subject = self.subject
    if (self.reply_reference is not None):
        reference = self.reply_reference
        subject = ('Re: %s' % subject)
    else:
        reference = self.reference
    if isinstance(reference, Group):
        (thread, created) = GroupEmailThread.objects.get_or_create(email=to, group=reference, defaults={
            'project': reference.project,
            'msgid': message_id,
        })
        if (not created):
            headers.setdefault('In-Reply-To', thread.msgid)
            headers.setdefault('References', thread.msgid)
    msg = EmailMultiAlternatives(subject=subject.splitlines()[0], body=self.__render_text_body(), from_email=self.from_email, to=(to,), cc=(cc or ()), bcc=(bcc or ()), headers=headers)
    html_body = self.__render_html_body()
    if html_body:
        msg.attach_alternative(html_body.decode('utf-8'), 'text/html')
    return msg