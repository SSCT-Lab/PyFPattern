

def _all_directories(self, dir):
    results = []
    results.append(dir)
    for (root, subdirs, files) in os.walk(dir, followlinks=True):
        if ('__init__.py' in files):
            for x in subdirs:
                results.append(os.path.join(root, x))
    return results
