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
            try:
                if (set(destination[key]) != set((destination[key] + source[key]))):
                    destination[key] = list(set((destination[key] + source[key])))
                    changed = True
            except TypeError:
                for new_dict in source[key]:
                    found = False
                    for old_dict in destination[key]:
                        if (('name' in old_dict.keys()) and ('name' in new_dict.keys())):
                            if (old_dict['name'] == new_dict['name']):
                                destination[key].remove(old_dict)
                                break
                        if (old_dict == new_dict):
                            found = True
                            break
                    if (not found):
                        destination[key].append(new_dict)
                        changed = True
        elif ((key not in destination.keys()) or (destination[key] != source[key])):
            destination[key] = value
            changed = True
    return (destination, changed)