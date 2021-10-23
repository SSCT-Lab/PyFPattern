

def get_pid(name):
    return [p.info['pid'] for p in psutil.process_iter(attrs=['pid', 'name']) if (p.info and p.info.get('name', None) and (p.info['name'].lower() == name.lower()))]
