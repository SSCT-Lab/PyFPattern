def _extract_from_url(self, url, video_id, fatal_if_no_video=True):
    req = sanitized_Request(url)
    req.add_header('User-Agent', self._CHROME_USER_AGENT)
    webpage = self._download_webpage(req, video_id)
    video_data = None
    BEFORE = '{swf.addParam(param[0], param[1]);});'
    AFTER = '.forEach(function(variable) {swf.addVariable(variable[0], variable[1]);});'
    m = re.search(((re.escape(BEFORE) + '(?:\n|\\\\n)(.*?)') + re.escape(AFTER)), webpage)
    if m:
        swf_params = m.group(1).replace('\\\\', '\\').replace('\\"', '"')
        data = dict(json.loads(swf_params))
        params_raw = compat_urllib_parse_unquote(data['params'])
        video_data = json.loads(params_raw)['video_data']

    def video_data_list2dict(video_data):
        ret = {
            
        }
        for item in video_data:
            format_id = item['stream_type']
            ret.setdefault(format_id, []).append(item)
        return ret
    if (not video_data):
        server_js_data = self._parse_json(self._search_regex('handleServerJS\\(({.+})\\);', webpage, 'server js data', default='{}'), video_id)
        for item in server_js_data.get('instances', []):
            if (item[1][0] == 'VideoConfig'):
                video_data = video_data_list2dict(item[2][0]['videoData'])
                break
    if (not video_data):
        if (not fatal_if_no_video):
            return (webpage, False)
        m_msg = re.search('class="[^"]*uiInterstitialContent[^"]*"><div>(.*?)</div>', webpage)
        if (m_msg is not None):
            raise ExtractorError(('The video is not available, Facebook said: "%s"' % m_msg.group(1)), expected=True)
        else:
            raise ExtractorError('Cannot parse data')
    formats = []
    for (format_id, f) in video_data.items():
        if (f and isinstance(f, dict)):
            f = [f]
        if ((not f) or (not isinstance(f, list))):
            continue
        for quality in ('sd', 'hd'):
            for src_type in ('src', 'src_no_ratelimit'):
                src = f[0].get(('%s_%s' % (quality, src_type)))
                if src:
                    preference = ((- 10) if (format_id == 'progressive') else 0)
                    if (quality == 'hd'):
                        preference += 5
                    formats.append({
                        'format_id': ('%s_%s_%s' % (format_id, quality, src_type)),
                        'url': src,
                        'preference': preference,
                    })
        dash_manifest = f[0].get('dash_manifest')
        if dash_manifest:
            formats.extend(self._parse_mpd_formats(compat_etree_fromstring(compat_urllib_parse_unquote_plus(dash_manifest))))
    if (not formats):
        raise ExtractorError('Cannot find video formats')
    self._sort_formats(formats)
    video_title = self._html_search_regex('<h2\\s+[^>]*class="uiHeaderTitle"[^>]*>([^<]*)</h2>', webpage, 'title', default=None)
    if (not video_title):
        video_title = self._html_search_regex('(?s)<span class="fbPhotosPhotoCaption".*?id="fbPhotoPageCaption"><span class="hasCaption">(.*?)</span>', webpage, 'alternative title', default=None)
        video_title = limit_length(video_title, 80)
    if (not video_title):
        video_title = ('Facebook video #%s' % video_id)
    uploader = clean_html(get_element_by_id('fbPhotoPageAuthorName', webpage))
    info_dict = {
        'id': video_id,
        'title': video_title,
        'formats': formats,
        'uploader': uploader,
    }
    return (webpage, info_dict)