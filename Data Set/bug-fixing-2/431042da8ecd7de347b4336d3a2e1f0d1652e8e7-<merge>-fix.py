

def merge(self, source, destination, changed):
    for (key, value) in source.items():
        if isinstance(value, dict):
            try:
                node = destination.setdefault(key, {
                    
                })
            except AttributeError:
                node = {
                    
                }
            finally:
                (_, changed) = self.merge(value, node, changed)
        elif (isinstance(value, list) and (key in destination.keys())):
            if (destination[key] != source[key]):
                destination[key] = source[key]
                changed = True
        elif ((key not in destination.keys()) or (destination[key] != source[key])):
            destination[key] = value
            changed = True
    return (destination, changed)
