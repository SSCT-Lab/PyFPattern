

def get_python_facts(self):
    self.facts['python'] = {
        'version': {
            'major': sys.version_info[0],
            'minor': sys.version_info[1],
            'micro': sys.version_info[2],
            'releaselevel': sys.version_info[3],
            'serial': sys.version_info[4],
        },
        'version_info': list(sys.version_info),
        'executable': sys.executable,
        'has_sslcontext': HAS_SSLCONTEXT,
    }
    try:
        self.facts['python']['type'] = sys.subversion[0]
    except AttributeError:
        self.facts['python']['type'] = None
