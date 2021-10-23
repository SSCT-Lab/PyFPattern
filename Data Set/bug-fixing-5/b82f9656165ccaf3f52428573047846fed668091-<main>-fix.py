def main():
    module = AnsibleModule(argument_spec=dict(username=dict(type='str'), password=dict(type='str', no_log=True), host=dict(type='str', default='localhost'), port=dict(type='int', default=25), sender=dict(type='str', default='root', aliases=['from']), to=dict(type='list', default=['root'], aliases=['recipients']), cc=dict(type='list', default=[]), bcc=dict(type='list', default=[]), subject=dict(type='str', required=True, aliases=['msg']), body=dict(type='str'), attach=dict(type='list', default=[]), headers=dict(type='list', default=[]), charset=dict(type='str', default='utf-8'), subtype=dict(type='str', default='plain', choices=['html', 'plain']), secure=dict(type='str', default='try', choices=['always', 'never', 'starttls', 'try']), timeout=dict(type='int', default=20)), required_together=[['password', 'username']])
    username = module.params.get('username')
    password = module.params.get('password')
    host = module.params.get('host')
    port = module.params.get('port')
    sender = module.params.get('sender')
    recipients = module.params.get('to')
    copies = module.params.get('cc')
    blindcopies = module.params.get('bcc')
    subject = module.params.get('subject')
    body = module.params.get('body')
    attach_files = module.params.get('attach')
    headers = module.params.get('headers')
    charset = module.params.get('charset')
    subtype = module.params.get('subtype')
    secure = module.params.get('secure')
    timeout = module.params.get('timeout')
    code = 0
    secure_state = False
    (sender_phrase, sender_addr) = parseaddr(sender)
    if (not body):
        body = subject
    try:
        if (secure != 'never'):
            try:
                smtp = smtplib.SMTP_SSL(host=host, timeout=timeout)
                (code, smtpmessage) = smtp.connect(host, port=port)
                secure_state = True
            except ssl.SSLError as e:
                if (secure == 'always'):
                    module.fail_json(rc=1, msg=('Unable to start an encrypted session to %s:%s: %s' % (host, port, to_native(e))), exception=traceback.format_exc())
            except:
                pass
        if (not secure_state):
            smtp = smtplib.SMTP(timeout=timeout)
            (code, smtpmessage) = smtp.connect(host, port=port)
    except smtplib.SMTPException as e:
        module.fail_json(rc=1, msg=('Unable to Connect %s:%s: %s' % (host, port, to_native(e))), exception=traceback.format_exc())
    try:
        smtp.ehlo()
    except smtplib.SMTPException as e:
        module.fail_json(rc=1, msg=('Helo failed for host %s:%s: %s' % (host, port, to_native(e))), exception=traceback.format_exc())
    if (int(code) > 0):
        if ((not secure_state) and (secure in ('starttls', 'try'))):
            if smtp.has_extn('STARTTLS'):
                try:
                    smtp.starttls()
                    secure_state = True
                except smtplib.SMTPException as e:
                    module.fail_json(rc=1, msg=('Unable to start an encrypted session to %s:%s: %s' % (host, port, to_native(e))), exception=traceback.format_exc())
                try:
                    smtp.ehlo()
                except smtplib.SMTPException as e:
                    module.fail_json(rc=1, msg=('Helo failed for host %s:%s: %s' % (host, port, to_native(e))), exception=traceback.format_exc())
            elif (secure == 'starttls'):
                module.fail_json(rc=1, msg=('StartTLS is not offered on server %s:%s' % (host, port)))
    if (username and password):
        if smtp.has_extn('AUTH'):
            try:
                smtp.login(username, password)
            except smtplib.SMTPAuthenticationError:
                module.fail_json(rc=1, msg=('Authentication to %s:%s failed, please check your username and/or password' % (host, port)))
            except smtplib.SMTPException:
                module.fail_json(rc=1, msg=('No Suitable authentication method was found on %s:%s' % (host, port)))
        else:
            module.fail_json(rc=1, msg=('No Authentication on the server at %s:%s' % (host, port)))
    if ((not secure_state) and (username and password)):
        module.warn('Username and Password was sent without encryption')
    msg = MIMEMultipart(_charset=charset)
    msg['From'] = formataddr((sender_phrase, sender_addr))
    msg['Subject'] = Header(subject, charset)
    msg.preamble = 'Multipart message'
    for header in headers:
        for hdr in [x.strip() for x in header.split('|')]:
            try:
                (h_key, h_val) = hdr.split('=')
                h_val = to_native(Header(h_val, charset))
                msg.add_header(h_key, h_val)
            except Exception:
                module.warn(("Skipping header '%s', unable to parse" % hdr))
    if ('X-Mailer' not in msg):
        msg.add_header('X-Mailer', 'Ansible mail module')
    addr_list = []
    for addr in [x.strip() for x in blindcopies]:
        addr_list.append(parseaddr(addr)[1])
    to_list = []
    for addr in [x.strip() for x in recipients]:
        to_list.append(formataddr(parseaddr(addr)))
        addr_list.append(parseaddr(addr)[1])
    msg['To'] = ', '.join(to_list)
    cc_list = []
    for addr in [x.strip() for x in copies]:
        cc_list.append(formataddr(parseaddr(addr)))
        addr_list.append(parseaddr(addr)[1])
    msg['Cc'] = ', '.join(cc_list)
    part = MIMEText((body + '\n\n'), _subtype=subtype, _charset=charset)
    msg.attach(part)
    for filename in attach_files:
        try:
            part = MIMEBase('application', 'octet-stream')
            with open(filename, 'rb') as fp:
                part.set_payload(fp.read())
            encoders.encode_base64(part)
            part.add_header('Content-disposition', 'attachment', filename=os.path.basename(filename))
            msg.attach(part)
        except Exception as e:
            module.fail_json(rc=1, msg=("Failed to send mail: can't attach file %s: %s" % (filename, to_native(e))), exception=traceback.format_exc())
    composed = msg.as_string()
    try:
        result = smtp.sendmail(sender_addr, set(addr_list), composed)
    except Exception as e:
        module.fail_json(rc=1, msg=("Failed to send mail to '%s': %s" % (', '.join(set(addr_list)), to_native(e))), exception=traceback.format_exc())
    smtp.quit()
    if result:
        for key in result:
            module.warn(("Failed to send mail to '%s': %s %s" % (key, result[key][0], result[key][1])))
        module.exit_json(msg='Failed to send mail to at least one recipient', result=result)
    module.exit_json(msg='Mail sent successfully', result=result)