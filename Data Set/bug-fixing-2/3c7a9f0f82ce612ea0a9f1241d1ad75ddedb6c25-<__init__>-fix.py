

def __init__(self):
    self.log = logging.getLogger('SiteManager')
    self.log.debug('SiteManager created.')
    self.sites = None
    gevent.spawn(self.saveTimer)
