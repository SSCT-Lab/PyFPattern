def message(self):
    encoding = (self.encoding or settings.DEFAULT_CHARSET)
    msg = SafeMIMEText(self.body, self.content_subtype, encoding)
    msg = self._create_message(msg)
    msg['Subject'] = self.subject
    msg['From'] = self.extra_headers.get('From', self.from_email)
    msg['To'] = self.extra_headers.get('To', ', '.join(map(force_text, self.to)))
    if self.cc:
        msg['Cc'] = ', '.join(map(force_text, self.cc))
    if self.reply_to:
        msg['Reply-To'] = self.extra_headers.get('Reply-To', ', '.join(map(force_text, self.reply_to)))
    header_names = [key.lower() for key in self.extra_headers]
    if ('date' not in header_names):
        msg['Date'] = formatdate(localtime=settings.EMAIL_USE_LOCALTIME)
    if ('message-id' not in header_names):
        msg['Message-ID'] = make_msgid(domain=DNS_NAME)
    for (name, value) in self.extra_headers.items():
        if (name.lower() in ('from', 'to')):
            continue
        msg[name] = value
    return msg