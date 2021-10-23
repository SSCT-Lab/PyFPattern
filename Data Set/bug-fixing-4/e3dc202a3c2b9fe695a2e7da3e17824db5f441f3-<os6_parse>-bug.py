def os6_parse(lines, indent=None, comment_tokens=None):
    sublevel_cmds = [re.compile('^vlan.*$'), re.compile('^stack.*$'), re.compile('^interface.*$'), re.compile('line (console|telnet|ssh).*$'), re.compile('ip ssh !(server).*$'), re.compile('ip (dhcp|vrf).*$'), re.compile('(ip|mac|management|arp) access-list.*$'), re.compile('ipv6 (dhcp|router).*$'), re.compile('mail-server.*$'), re.compile('vpc domain.*$'), re.compile('router.*$'), re.compile('route-map.*$'), re.compile('policy-map.*$'), re.compile('class-map match-all.*$'), re.compile('captive-portal.*$'), re.compile('admin-profile.*$'), re.compile('link-dependency group.*$'), re.compile('banner motd.*$'), re.compile('openflow.*$'), re.compile('support-assist.*$'), re.compile('(radius-server|tacacs-server) host.*$')]
    childline = re.compile('^exit$')
    config = list()
    inSubLevel = False
    parent = None
    children = list()
    subcommandcount = 0
    for line in str(lines).split('\n'):
        text = str(re.sub('([{};])', '', line)).strip()
        cfg = ConfigLine(text)
        cfg.raw = line
        if ((not text) or ignore_line(text, comment_tokens)):
            parent = None
            children = list()
            inSubLevel = False
            continue
        if (inSubLevel is False):
            for pr in sublevel_cmds:
                if pr.match(line):
                    parent = cfg
                    config.append(parent)
                    inSubLevel = True
                    continue
            if (parent is None):
                config.append(cfg)
        elif (inSubLevel and childline.match(line)):
            parent.children = children
            inSubLevel = False
            children = list()
            parent = None
        elif inSubLevel:
            children.append(cfg)
            cfg.parents = [parent]
            config.append(cfg)
        else:
            config.append(cfg)
    return config