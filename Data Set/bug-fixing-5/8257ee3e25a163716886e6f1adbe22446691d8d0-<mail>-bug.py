def mail(subject='Ansible error mail', sender=None, to=None, cc=None, bcc=None, body=None, smtphost=None):
    if (sender is None):
        sender = '<root>'
    if (to is None):
        to = 'root'
    if (smtphost is None):
        smtphost = os.getenv('SMTPHOST', 'localhost')
    if (body is None):
        body = subject
    smtp = smtplib.SMTP(smtphost)
    b_sender = to_bytes(sender)
    b_to = to_bytes(to)
    b_cc = to_bytes(cc)
    b_bcc = to_bytes(bcc)
    b_subject = to_bytes(subject)
    b_body = to_bytes(body)
    b_content = (b'From: %s\n' % b_sender)
    b_content += (b'To: %s\n' % b_to)
    if cc:
        b_content += (b'Cc: %s\n' % b_cc)
    b_content += (b'Subject: %s\n\n' % b_subject)
    b_content += b_body
    b_addresses = b_to.split(b',')
    if b_cc:
        b_addresses += b_cc.split(b',')
    if b_bcc:
        b_addresses += b_bcc.split(b',')
    for b_address in b_addresses:
        smtp.sendmail(b_sender, b_address, b_content)
    smtp.quit()