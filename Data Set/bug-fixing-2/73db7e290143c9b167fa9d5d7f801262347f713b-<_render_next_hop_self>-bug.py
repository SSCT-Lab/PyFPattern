

def _render_next_hop_self(self, item, config=None):
    cmd = ('neighbor %s activate' % item['neighbor'])
    if (item['next_hop_self'] is False):
        if ((not config) or (cmd in config)):
            cmd = ('no %s' % cmd)
            return cmd
    elif ((not config) or (cmd not in config)):
        return cmd
