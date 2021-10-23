@staticmethod
def _extract_urls(webpage):
    return [url for (_, url) in re.findall('<iframe[^>]+src=(["\\\'])((?:https?:)?//(?:www\\.)?vessel\\.com/embed/[0-9a-zA-Z]+.*?)\\1', webpage)]