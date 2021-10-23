

@classmethod
def _build_brighcove_url_from_js(cls, object_js):
    m = re.search('(?x)customBC.\\createVideo\\(\n                .*?                                                  # skipping width and height\n                ["\\\'](?P<playerID>\\d+)["\\\']\\s*,\\s*                   # playerID\n                ["\\\'](?P<playerKey>AQ[^"\\\']{48})[^"\\\']*["\\\']\\s*,\\s*  # playerKey begins with AQ and is 50 characters\n                                                                     # in length, however it\'s appended to itself\n                                                                     # in places, so truncate\n                ["\\\'](?P<videoID>\\d+)["\\\']                           # @videoPlayer\n            ', object_js)
    if m:
        return cls._make_brightcove_url(m.groupdict())
