def count_nodes(module, tree, xpath, namespaces):
    ' Return the count of nodes matching the xpath '
    hits = tree.xpath(('count(/%s)' % xpath), namespaces=namespaces)
    finish(module, tree, xpath, namespaces, changed=False, msg=int(hits), hitcount=int(hits))