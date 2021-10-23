def os6_parse(lines, indent=None, comment_tokens=None):
    sublevel_cmds = [re.compile('^vlan.*$'), re.compile('^stack.*$'), re.compile('^interface.*$'), re.compile('datacenter-bridging.*$'), re.compile('line (console|telnet|ssh).*$'), re.compile('ip ssh !(server).*$'), re.compile('ip (dhcp|vrf).*$'), re.compile('(ip|mac|management|arp) access-list.*$'), re.compile('ipv6 (dhcp|router).*$'), re.compile('mail-server.*$'), re.compile('vpc domain.*$'), re.compile('router.*$'), re.compile('route-map.*$'), re.compile('policy-map.*$'), re.compile('class-map match-all.*$'), re.compile('captive-portal.*$'), re.compile('admin-profile.*$'), re.compile('link-dependency group.*$'), re.compile('banner motd.*$'), re.compile('openflow.*$'), re.compile('support-assist.*$'), re.compile('template.*$'), re.compile('address-family.*$'), re.compile('spanning-tree mst configuration.*$'), re.compile('logging.*$'), re.compile('(radius-server|tacacs-server) host.*$')]
    childline = re.compile('^exit$')
    config = list()
    parent = list()
    children = []
    parent_match = False
    for line in str(lines).split('\n'):
        text = str(re.sub('([{};])', '', line)).strip()
        cfg = ConfigLine(text)
        cfg.raw = line
        if ((not text) or ignore_line(text, comment_tokens)):
            parent = list()
            children = []
            continue
        else:
            parent_match = False
            for pr in sublevel_cmds:
                if pr.match(line):
                    if (len(parent) != 0):
                        cfg.parents.extend(parent)
                    parent.append(cfg)
                    config.append(cfg)
                    if children:
                        children.insert((len(parent) - 1), [])
                        children[(len(parent) - 2)].append(cfg)
                    parent_match = True
                    continue
            if childline.match(line):
                if children:
                    parent[(len(children) - 1)].children.extend(children[(len(children) - 1)])
                    if (len(children) > 1):
                        parent[(len(children) - 2)].children.extend(parent[(len(children) - 1)].children)
                    cfg.parents.extend(parent)
                    children.pop()
                    parent.pop()
                if (not children):
                    children = list()
                    if parent:
                        cfg.parents.extend(parent)
                    parent = list()
                    config.append(cfg)
            elif ((parent_match is False) and (len(parent) > 0)):
                if (not children):
                    cfglist = [cfg]
                    children.append(cfglist)
                else:
                    children[(len(parent) - 1)].append(cfg)
                cfg.parents.extend(parent)
                config.append(cfg)
            elif (not parent):
                config.append(cfg)
    return config