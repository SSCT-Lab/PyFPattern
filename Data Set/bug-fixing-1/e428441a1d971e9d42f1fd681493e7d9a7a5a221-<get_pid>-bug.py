

def get_pid(name):
    return [p.info['pid'] for p in psutil.process_iter(attrs=['pid', 'name']) if (name == p.info['name'])]
