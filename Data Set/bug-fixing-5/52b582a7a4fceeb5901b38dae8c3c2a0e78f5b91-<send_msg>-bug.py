def send_msg(msg, server='localhost', port='6667', channel=None, nick_to=None, key=None, topic=None, nick='ansible', color='none', passwd=False, timeout=30, use_ssl=False, part=True, style=None):
    'send message to IRC'
    nick_to = ([] if (nick_to is None) else nick_to)
    colornumbers = {
        'white': '00',
        'black': '01',
        'blue': '02',
        'green': '03',
        'red': '04',
        'brown': '05',
        'purple': '06',
        'orange': '07',
        'yellow': '08',
        'light_green': '09',
        'teal': '10',
        'light_cyan': '11',
        'light_blue': '12',
        'pink': '13',
        'gray': '14',
        'light_gray': '15',
    }
    stylechoices = {
        'bold': '\x02',
        'underline': '\x1f',
        'reverse': '\x16',
        'italic': '\x1d',
    }
    try:
        styletext = stylechoices[style]
    except Exception:
        styletext = ''
    try:
        colornumber = colornumbers[color]
        colortext = ('\x03' + colornumber)
    except Exception:
        colortext = ''
    message = ((styletext + colortext) + msg)
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if use_ssl:
        irc = ssl.wrap_socket(irc)
    irc.connect((server, int(port)))
    if passwd:
        irc.send(to_bytes(('PASS %s\r\n' % passwd)))
    irc.send(to_bytes(('NICK %s\r\n' % nick)))
    irc.send(to_bytes(('USER %s %s %s :ansible IRC\r\n' % (nick, nick, nick))))
    motd = ''
    start = time.time()
    while 1:
        motd += to_native(irc.recv(1024))
        match = re.search('^:\\S+ 00[1-4] (?P<nick>\\S+) :', motd, flags=re.M)
        if match:
            nick = match.group('nick')
            break
        elif ((time.time() - start) > timeout):
            raise Exception('Timeout waiting for IRC server welcome response')
        time.sleep(0.5)
    if key:
        irc.send(to_bytes(('JOIN %s %s\r\n' % (channel, key))))
    else:
        irc.send(to_bytes(('JOIN %s\r\n' % channel)))
    join = ''
    start = time.time()
    while 1:
        join += to_native(irc.recv(1024))
        if re.search(('^:\\S+ 366 %s %s :' % (nick, channel)), join, flags=re.M):
            break
        elif ((time.time() - start) > timeout):
            raise Exception('Timeout waiting for IRC JOIN response')
        time.sleep(0.5)
    if (topic is not None):
        irc.send(to_bytes(('TOPIC %s :%s\r\n' % (channel, topic))))
        time.sleep(1)
    if nick_to:
        for nick in nick_to:
            irc.send(to_bytes(('PRIVMSG %s :%s\r\n' % (nick, message))))
    if channel:
        irc.send(to_bytes(('PRIVMSG %s :%s\r\n' % (channel, message))))
    time.sleep(1)
    if part:
        irc.send(to_bytes(('PART %s\r\n' % channel)))
        irc.send(to_bytes('QUIT\r\n'))
        time.sleep(1)
    irc.close()