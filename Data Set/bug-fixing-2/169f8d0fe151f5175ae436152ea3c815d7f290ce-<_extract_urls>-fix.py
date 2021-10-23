

@staticmethod
def _extract_urls(webpage):
    return [mobj.group('url') for mobj in re.finditer('<script[^>]+\\bsrc=(["\\\'])(?P<url>(?:https?:)?//embed\\.(?:cloudflarestream\\.com|videodelivery\\.net)/embed/[^/]+\\.js\\?.*?\\bvideo=[\\da-f]+?.*?)\\1', webpage)]
