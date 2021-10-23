def _find_video_id(self, webpage):
    res_id = ['"video_id"\\s*:\\s*"(.*?)"', 'class="hero-poster[^"]*?"[^>]*id="(.+?)"', 'data-video-id="(.+?)"', '<object id="vid_(.+?)"', '<meta name="og:image" content=".*/(.+?)-(.+?)/.+.jpg"', 'videoId&quot;\\s*:\\s*&quot;(.+?)&quot;', 'videoId["\\\']\\s*:\\s*["\\\']([^"\\\']+?)["\\\']']
    return self._search_regex(res_id, webpage, 'video id', default=None)