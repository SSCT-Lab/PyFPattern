

def sanitize_xml(data):
    tree = fromstring(to_bytes(deepcopy(data), errors='surrogate_then_replace'))
    for element in tree.getiterator():
        attribute = element.attrib
        if attribute:
            for key in list(attribute):
                if (key not in IGNORE_XML_ATTRIBUTE):
                    attribute.pop(key)
    return to_text(tostring(tree), errors='surrogate_then_replace').strip()
