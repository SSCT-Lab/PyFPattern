

@staticmethod
def _extract_urls(webpage):
    return [m.group('url') for m in re.finditer('<iframe[^>]+src=(["\\\'])(?P<url>(?:https?://)?(?:www\\.)?20min\\.ch/videoplayer/videoplayer.html\\?.*?\\bvideoId@\\d+.*?)\\1', webpage)]
