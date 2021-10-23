

def POS_tree(root, light=False, flat=False):
    'Helper: generate a POS tree for a root token. The doc must have\n    `merge_ents(doc)` ran on it.\n    '
    subtree = format_POS(root, light=light, flat=flat)
    for c in root.children:
        subtree['modifiers'].append(POS_tree(c))
    return subtree
