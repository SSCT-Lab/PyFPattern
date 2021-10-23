

def _real_extract(self, url):
    if url.startswith('//'):
        return {
            '_type': 'url',
            'url': (self.http_scheme() + url),
        }
    parsed_url = compat_urlparse.urlparse(url)
    if (not parsed_url.scheme):
        default_search = self._downloader.params.get('default_search')
        if (default_search is None):
            default_search = 'fixup_error'
        if (default_search in ('auto', 'auto_warning', 'fixup_error')):
            if ('/' in url):
                self._downloader.report_warning("The url doesn't specify the protocol, trying with http")
                return self.url_result(('http://' + url))
            elif (default_search != 'fixup_error'):
                if (default_search == 'auto_warning'):
                    if re.match('^(?:url|URL)$', url):
                        raise ExtractorError(('Invalid URL:  %r . Call youtube-dl like this:  youtube-dl -v "https://www.youtube.com/watch?v=BaW_jenozKc"  ' % url), expected=True)
                    else:
                        self._downloader.report_warning(('Falling back to youtube search for  %s . Set --default-search "auto" to suppress this warning.' % url))
                return self.url_result(('ytsearch:' + url))
        if (default_search in ('error', 'fixup_error')):
            raise ExtractorError(('%r is not a valid URL. Set --default-search "ytsearch" (or run  youtube-dl "ytsearch:%s" ) to search YouTube' % (url, url)), expected=True)
        else:
            if (':' not in default_search):
                default_search += ':'
            return self.url_result((default_search + url))
    (url, smuggled_data) = unsmuggle_url(url)
    force_videoid = None
    is_intentional = (smuggled_data and smuggled_data.get('to_generic'))
    if (smuggled_data and ('force_videoid' in smuggled_data)):
        force_videoid = smuggled_data['force_videoid']
        video_id = force_videoid
    else:
        video_id = self._generic_id(url)
    self.to_screen(('%s: Requesting header' % video_id))
    head_req = HEADRequest(url)
    head_response = self._request_webpage(head_req, video_id, note=False, errnote=('Could not send HEAD request to %s' % url), fatal=False)
    if (head_response is not False):
        new_url = compat_str(head_response.geturl())
        if (url != new_url):
            self.report_following_redirect(new_url)
            if force_videoid:
                new_url = smuggle_url(new_url, {
                    'force_videoid': force_videoid,
                })
            return self.url_result(new_url)
    full_response = None
    if (head_response is False):
        request = sanitized_Request(url)
        request.add_header('Accept-Encoding', '*')
        full_response = self._request_webpage(request, video_id)
        head_response = full_response
    info_dict = {
        'id': video_id,
        'title': self._generic_title(url),
        'upload_date': unified_strdate(head_response.headers.get('Last-Modified')),
    }
    content_type = head_response.headers.get('Content-Type', '').lower()
    m = re.match('^(?P<type>audio|video|application(?=/(?:ogg$|(?:vnd\\.apple\\.|x-)?mpegurl)))/(?P<format_id>[^;\\s]+)', content_type)
    if m:
        format_id = compat_str(m.group('format_id'))
        if format_id.endswith('mpegurl'):
            formats = self._extract_m3u8_formats(url, video_id, 'mp4')
        elif (format_id == 'f4m'):
            formats = self._extract_f4m_formats(url, video_id)
        else:
            formats = [{
                'format_id': format_id,
                'url': url,
                'vcodec': ('none' if (m.group('type') == 'audio') else None),
            }]
            info_dict['direct'] = True
        self._sort_formats(formats)
        info_dict['formats'] = formats
        return info_dict
    if ((not self._downloader.params.get('test', False)) and (not is_intentional)):
        force = self._downloader.params.get('force_generic_extractor', False)
        self._downloader.report_warning(('%s on generic information extractor.' % ('Forcing' if force else 'Falling back')))
    if (not full_response):
        request = sanitized_Request(url)
        request.add_header('Accept-Encoding', '*')
        full_response = self._request_webpage(request, video_id)
    first_bytes = full_response.read(512)
    if first_bytes.startswith(b'#EXTM3U'):
        info_dict['formats'] = self._extract_m3u8_formats(url, video_id, 'mp4')
        self._sort_formats(info_dict['formats'])
        return info_dict
    if (not is_html(first_bytes)):
        self._downloader.report_warning('URL could be a direct video link, returning it as such.')
        info_dict.update({
            'direct': True,
            'url': url,
        })
        return info_dict
    webpage = self._webpage_read_content(full_response, url, video_id, prefix=first_bytes)
    self.report_extraction(video_id)
    try:
        doc = compat_etree_fromstring(webpage.encode('utf-8'))
        if (doc.tag == 'rss'):
            return self._extract_rss(url, video_id, doc)
        elif (doc.tag == 'SmoothStreamingMedia'):
            info_dict['formats'] = self._parse_ism_formats(doc, url)
            self._sort_formats(info_dict['formats'])
            return info_dict
        elif re.match('^(?:{[^}]+})?smil$', doc.tag):
            smil = self._parse_smil(doc, url, video_id)
            self._sort_formats(smil['formats'])
            return smil
        elif (doc.tag == '{http://xspf.org/ns/0/}playlist'):
            return self.playlist_result(self._parse_xspf(doc, video_id, xspf_url=url, xspf_base_url=compat_str(full_response.geturl())), video_id)
        elif re.match('(?i)^(?:{[^}]+})?MPD$', doc.tag):
            info_dict['formats'] = self._parse_mpd_formats(doc, mpd_base_url=compat_str(full_response.geturl()).rpartition('/')[0], mpd_url=url)
            self._sort_formats(info_dict['formats'])
            return info_dict
        elif re.match('^{http://ns\\.adobe\\.com/f4m/[12]\\.0}manifest$', doc.tag):
            info_dict['formats'] = self._parse_f4m_formats(doc, url, video_id)
            self._sort_formats(info_dict['formats'])
            return info_dict
    except compat_xml_parse_error:
        pass
    camtasia_res = self._extract_camtasia(url, video_id, webpage)
    if (camtasia_res is not None):
        return camtasia_res
    webpage = compat_urllib_parse_unquote(webpage)
    video_title = (self._og_search_title(webpage, default=None) or self._html_search_regex('(?s)<title>(.*?)</title>', webpage, 'video title', default='video'))
    age_limit = self._rta_search(webpage)
    AGE_LIMIT_MARKERS = ['Proudly Labeled <a href="http://www\\.rtalabel\\.org/" title="Restricted to Adults">RTA</a>']
    if any((re.search(marker, webpage) for marker in AGE_LIMIT_MARKERS)):
        age_limit = 18
    video_uploader = self._search_regex('^(?:https?://)?([^/]*)/.*', url, 'video uploader')
    video_description = self._og_search_description(webpage, default=None)
    video_thumbnail = self._og_search_thumbnail(webpage, default=None)
    info_dict.update({
        'title': video_title,
        'description': video_description,
        'thumbnail': video_thumbnail,
        'age_limit': age_limit,
    })
    bc_urls = BrightcoveLegacyIE._extract_brightcove_urls(webpage)
    if bc_urls:
        entries = [{
            '_type': 'url',
            'url': smuggle_url(bc_url, {
                'Referer': url,
            }),
            'ie_key': 'BrightcoveLegacy',
        } for bc_url in bc_urls]
        return {
            '_type': 'playlist',
            'title': video_title,
            'id': video_id,
            'entries': entries,
        }
    bc_urls = BrightcoveNewIE._extract_urls(self, webpage)
    if bc_urls:
        return self.playlist_from_matches(bc_urls, video_id, video_title, getter=(lambda x: smuggle_url(x, {
            'referrer': url,
        })), ie='BrightcoveNew')
    nexx_urls = NexxIE._extract_urls(webpage)
    if nexx_urls:
        return self.playlist_from_matches(nexx_urls, video_id, video_title, ie=NexxIE.ie_key())
    nexx_embed_urls = NexxEmbedIE._extract_urls(webpage)
    if nexx_embed_urls:
        return self.playlist_from_matches(nexx_embed_urls, video_id, video_title, ie=NexxEmbedIE.ie_key())
    tp_urls = ThePlatformIE._extract_urls(webpage)
    if tp_urls:
        return self.playlist_from_matches(tp_urls, video_id, video_title, ie='ThePlatform')
    vessel_urls = VesselIE._extract_urls(webpage)
    if vessel_urls:
        return self.playlist_from_matches(vessel_urls, video_id, video_title, ie=VesselIE.ie_key())
    matches = re.findall('<iframe[^>]+?src="((?:https?:)?//(?:(?:www|static)\\.)?rtl\\.nl/(?:system/videoplayer/[^"]+(?:video_)?)?embed[^"]+)"', webpage)
    if matches:
        return self.playlist_from_matches(matches, video_id, video_title, ie='RtlNl')
    vimeo_urls = VimeoIE._extract_urls(url, webpage)
    if vimeo_urls:
        return self.playlist_from_matches(vimeo_urls, video_id, video_title, ie=VimeoIE.ie_key())
    vid_me_embed_url = self._search_regex('src=[\\\'"](https?://vid\\.me/[^\\\'"]+)[\\\'"]', webpage, 'vid.me embed', default=None)
    if (vid_me_embed_url is not None):
        return self.url_result(vid_me_embed_url, 'Vidme')
    youtube_urls = YoutubeIE._extract_urls(webpage)
    if youtube_urls:
        return self.playlist_from_matches(youtube_urls, video_id, video_title, ie=YoutubeIE.ie_key())
    matches = DailymotionIE._extract_urls(webpage)
    if matches:
        return self.playlist_from_matches(matches, video_id, video_title)
    m = re.search('<iframe[^>]+?src=(["\\\'])(?P<url>(?:https?:)?//(?:www\\.)?dailymotion\\.[a-z]{2,3}/widget/jukebox\\?.+?)\\1', webpage)
    if m:
        playlists = re.findall('list\\[\\]=/playlist/([^/]+)/', unescapeHTML(m.group('url')))
        if playlists:
            return self.playlist_from_matches(playlists, video_id, video_title, (lambda p: ('//dailymotion.com/playlist/%s' % p)))
    dailymail_urls = DailyMailIE._extract_urls(webpage)
    if dailymail_urls:
        return self.playlist_from_matches(dailymail_urls, video_id, video_title, ie=DailyMailIE.ie_key())
    wistia_url = WistiaIE._extract_url(webpage)
    if wistia_url:
        return {
            '_type': 'url_transparent',
            'url': self._proto_relative_url(wistia_url),
            'ie_key': WistiaIE.ie_key(),
            'uploader': video_uploader,
        }
    svt_url = SVTIE._extract_url(webpage)
    if svt_url:
        return self.url_result(svt_url, 'SVT')
    mobj = re.search('<meta property="og:url"[^>]*?content="(.*?bandcamp\\.com.*?)"', webpage)
    if (mobj is not None):
        burl = unescapeHTML(mobj.group(1))
        return self.url_result(burl)
    mobj = re.search('<iframe[^>]+?src=(["\\\'])(?P<url>(?:https?:)?//(?:cache\\.)?vevo\\.com/.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'))
    mobj = re.search('<(?:iframe[^>]+?src|param[^>]+?value)=(["\\\'])(?P<url>(?:https?:)?//(?:www\\.)?viddler\\.com/(?:embed|player)/.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'))
    mobj = re.search('<iframe[^>]+src=(["\\\'])(?P<url>(?:https?:)?//graphics8\\.nytimes\\.com/bcvideo/[^/]+/iframe/embed\\.html.+?)\\1>', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'))
    mobj = re.search('<iframe[^>]+src=(["\\\'])(?P<url>(?:https?:)?//html5-player\\.libsyn\\.com/embed/.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'))
    mobj = (re.search('player\\.ooyala\\.com/[^"?]+[?#][^"]*?(?:embedCode|ec)=(?P<ec>[^"&]+)', webpage) or re.search('OO\\.Player\\.create\\([\\\'"].*?[\\\'"],\\s*[\\\'"](?P<ec>.{32})[\\\'"]', webpage) or re.search('OO\\.Player\\.create\\.apply\\(\\s*OO\\.Player\\s*,\\s*op\\(\\s*\\[\\s*[\\\'"][^\\\'"]*[\\\'"]\\s*,\\s*[\\\'"](?P<ec>.{32})[\\\'"]', webpage) or re.search('SBN\\.VideoLinkset\\.ooyala\\([\\\'"](?P<ec>.{32})[\\\'"]\\)', webpage) or re.search('data-ooyala-video-id\\s*=\\s*[\\\'"](?P<ec>.{32})[\\\'"]', webpage))
    if (mobj is not None):
        embed_token = self._search_regex('embedToken[\\\'"]?\\s*:\\s*[\\\'"]([^\\\'"]+)', webpage, 'ooyala embed token', default=None)
        return OoyalaIE._build_url_result(smuggle_url(mobj.group('ec'), {
            'domain': url,
            'embed_token': embed_token,
        }))
    mobj = re.search('SBN\\.VideoLinkset\\.entryGroup\\((\\[.*?\\])', webpage)
    if (mobj is not None):
        embeds = self._parse_json(mobj.group(1), video_id, fatal=False)
        if embeds:
            return self.playlist_from_matches(embeds, video_id, video_title, getter=(lambda v: OoyalaIE._url_for_embed_code(smuggle_url(v['provider_video_id'], {
                'domain': url,
            }))), ie='Ooyala')
    mobj = re.search('<iframe .*?src="(http://www\\.aparat\\.com/video/[^"]+)"', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group(1), 'Aparat')
    mobj = re.search('<iframe .*?src="(http://mpora\\.(?:com|de)/videos/[^"]+)"', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group(1), 'Mpora')
    mobj = re.search('(?x)<(?:pagespeed_)?iframe[^>]+?src=(["\\\'])\n                    (?P<url>http://(?:(?:embed|www)\\.)?\n                        (?:novamov\\.com|\n                           nowvideo\\.(?:ch|sx|eu|at|ag|co)|\n                           videoweed\\.(?:es|com)|\n                           movshare\\.(?:net|sx|ag)|\n                           divxstage\\.(?:eu|net|ch|co|at|ag))\n                        /embed\\.php.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'))
    facebook_urls = FacebookIE._extract_urls(webpage)
    if facebook_urls:
        return self.playlist_from_matches(facebook_urls, video_id, video_title)
    mobj = re.search('<iframe[^>]+?src=(["\\\'])(?P<url>https?://vk\\.com/video_ext\\.php.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'), 'VK')
    mobj = re.search('<iframe[^>]+?src=(["\\\'])(?P<url>https?://(?:odnoklassniki|ok)\\.ru/videoembed/.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'), 'Odnoklassniki')
    mobj = re.search('<embed[^>]+?src=(["\\\'])(?P<url>https?://(?:www\\.)?ivi\\.ru/video/player.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'), 'Ivi')
    mobj = re.search('<iframe[^>]+?src=(["\\\'])(?P<url>https?://embed\\.live\\.huffingtonpost\\.com/.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'), 'HuffPost')
    mobj = re.search('class=["\\\']embedly-card["\\\'][^>]href=["\\\'](?P<url>[^"\\\']+)', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'))
    mobj = re.search('class=["\\\']embedly-embed["\\\'][^>]src=["\\\'][^"\\\']*url=(?P<url>[^&]+)', webpage)
    if (mobj is not None):
        return self.url_result(compat_urllib_parse_unquote(mobj.group('url')))
    matches = re.findall('<iframe[^>]+?src="(https?://(?:www\\.)?funnyordie\\.com/embed/[^"]+)"', webpage)
    if matches:
        return self.playlist_from_matches(matches, video_id, video_title, getter=unescapeHTML, ie='FunnyOrDie')
    matches = re.findall('setPlaylist\\("(https?://www\\.bbc\\.co\\.uk/iplayer/[^/]+/[\\da-z]{8})"\\)', webpage)
    if matches:
        return self.playlist_from_matches(matches, video_id, video_title, ie='BBCCoUk')
    rutv_url = RUTVIE._extract_url(webpage)
    if rutv_url:
        return self.url_result(rutv_url, 'RUTV')
    tvc_url = TVCIE._extract_url(webpage)
    if tvc_url:
        return self.url_result(tvc_url, 'TVC')
    sportbox_urls = SportBoxEmbedIE._extract_urls(webpage)
    if sportbox_urls:
        return self.playlist_from_matches(sportbox_urls, video_id, video_title, ie='SportBoxEmbed')
    xhamster_urls = XHamsterEmbedIE._extract_urls(webpage)
    if xhamster_urls:
        return self.playlist_from_matches(xhamster_urls, video_id, video_title, ie='XHamsterEmbed')
    tnaflix_urls = TNAFlixNetworkEmbedIE._extract_urls(webpage)
    if tnaflix_urls:
        return self.playlist_from_matches(tnaflix_urls, video_id, video_title, ie=TNAFlixNetworkEmbedIE.ie_key())
    pornhub_urls = PornHubIE._extract_urls(webpage)
    if pornhub_urls:
        return self.playlist_from_matches(pornhub_urls, video_id, video_title, ie=PornHubIE.ie_key())
    drtuber_urls = DrTuberIE._extract_urls(webpage)
    if drtuber_urls:
        return self.playlist_from_matches(drtuber_urls, video_id, video_title, ie=DrTuberIE.ie_key())
    redtube_urls = RedTubeIE._extract_urls(webpage)
    if redtube_urls:
        return self.playlist_from_matches(redtube_urls, video_id, video_title, ie=RedTubeIE.ie_key())
    mobj = re.search('<iframe[^>]+?src=(["\\\'])(?P<url>(?:https?:)?//cloud\\.tvigle\\.ru/video/.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'), 'Tvigle')
    mobj = re.search('<iframe[^>]+?src=(["\\\'])(?P<url>https?://embed(?:-ssl)?\\.ted\\.com/.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'), 'TED')
    ustream_url = UstreamIE._extract_url(webpage)
    if ustream_url:
        return self.url_result(ustream_url, UstreamIE.ie_key())
    mobj = re.search('<(?:script|iframe) [^>]*?src="(?P<url>http://www\\.arte\\.tv/(?:playerv2/embed|arte_vp/index)[^"]+)"', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'), 'ArteTVEmbed')
    mobj = re.search('<iframe[^>]+?src=(["\\\'])(?P<url>(?:https?://)?embed\\.francetv\\.fr/\\?ue=.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'))
    smotri_url = SmotriIE._extract_url(webpage)
    if smotri_url:
        return self.url_result(smotri_url, 'Smotri')
    myvi_url = MyviIE._extract_url(webpage)
    if myvi_url:
        return self.url_result(myvi_url)
    soundcloud_urls = SoundcloudIE._extract_urls(webpage)
    if soundcloud_urls:
        return self.playlist_from_matches(soundcloud_urls, video_id, video_title, getter=unescapeHTML, ie=SoundcloudIE.ie_key())
    tunein_urls = TuneInBaseIE._extract_urls(webpage)
    if tunein_urls:
        return self.playlist_from_matches(tunein_urls, video_id, video_title)
    mtvservices_url = MTVServicesEmbeddedIE._extract_url(webpage)
    if mtvservices_url:
        return self.url_result(mtvservices_url, ie='MTVServicesEmbedded')
    mobj = re.search('<iframe[^>]+?src=(["\\\'])(?P<url>https?://(?:screen|movies)\\.yahoo\\.com/.+?\\.html\\?format=embed)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'), 'Yahoo')
    mobj = re.search('(?x)\n            (?:\n                <meta\\s+property="og:video"\\s+content=|\n                <iframe[^>]+?src=\n            )\n            (["\\\'])(?P<url>https?://(?:www\\.)?sbs\\.com\\.au/ondemand/video/.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'), 'SBS')
    mobj = re.search('<iframe[^>]+?src=(["\\\'])(?P<url>https?://player\\.cinchcast\\.com/.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'), 'Cinchcast')
    mobj = re.search('<iframe[^>]+?src=(["\\\'])(?P<url>https?://m(?:lb)?\\.mlb\\.com/shared/video/embed/embed\\.html\\?.+?)\\1', webpage)
    if (not mobj):
        mobj = re.search('data-video-link=["\\\'](?P<url>http://m.mlb.com/video/[^"\\\']+)', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'), 'MLB')
    mobj = re.search(('<(?:iframe|script)[^>]+?src=(["\\\'])(?P<url>%s)\\1' % CondeNastIE.EMBED_URL), webpage)
    if (mobj is not None):
        return self.url_result(self._proto_relative_url(mobj.group('url'), scheme='http:'), 'CondeNast')
    mobj = re.search('<iframe[^>]+src="(?P<url>https?://(?:new\\.)?livestream\\.com/[^"]+/player[^"]+)"', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'), 'Livestream')
    mobj = re.search('<iframe[^>]+src="(?P<url>https?://(?:www\\.)?zapiks\\.fr/index\\.php\\?.+?)"', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'), 'Zapiks')
    kaltura_url = KalturaIE._extract_url(webpage)
    if kaltura_url:
        return self.url_result(smuggle_url(kaltura_url, {
            'source_url': url,
        }), KalturaIE.ie_key())
    eagleplatform_url = EaglePlatformIE._extract_url(webpage)
    if eagleplatform_url:
        return self.url_result(smuggle_url(eagleplatform_url, {
            'referrer': url,
        }), EaglePlatformIE.ie_key())
    mobj = re.search('<iframe[^>]+src="https?://(?P<host>media\\.clipyou\\.ru)/index/player\\?.*\\brecord_id=(?P<id>\\d+).*"', webpage)
    if (mobj is not None):
        return self.url_result(('eagleplatform:%(host)s:%(id)s' % mobj.groupdict()), 'EaglePlatform')
    pladform_url = PladformIE._extract_url(webpage)
    if pladform_url:
        return self.url_result(pladform_url)
    videomore_url = VideomoreIE._extract_url(webpage)
    if videomore_url:
        return self.url_result(videomore_url)
    webcaster_url = WebcasterFeedIE._extract_url(self, webpage)
    if webcaster_url:
        return self.url_result(webcaster_url, ie=WebcasterFeedIE.ie_key())
    mobj = re.search('<script[^>]+data-config=(["\\\'])(?P<url>(?:https?:)?//config\\.playwire\\.com/.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'))
    mobj = re.search('<meta[^>]+property="og:video"[^>]+content="https?://embed\\.5min\\.com/(?P<id>[0-9]+)/?', webpage)
    if (mobj is not None):
        return self.url_result(('5min:%s' % mobj.group('id')), 'FiveMin')
    mobj = re.search('<(?:iframe[^>]+src|param[^>]+value)=(["\\\'])(?P<url>(?:https?:)?//embed\\.crooksandliars\\.com/(?:embed|v)/.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(mobj.group('url'))
    nbc_sports_url = NBCSportsVPlayerIE._extract_url(webpage)
    if nbc_sports_url:
        return self.url_result(nbc_sports_url, 'NBCSportsVPlayer')
    nbc_news_embed_url = re.search('<iframe[^>]+src=(["\\\'])(?P<url>(?:https?:)?//www\\.nbcnews\\.com/widget/video-embed/[^"\\\']+)\\1', webpage)
    if nbc_news_embed_url:
        return self.url_result(nbc_news_embed_url.group('url'), 'NBCNews')
    google_drive_url = GoogleDriveIE._extract_url(webpage)
    if google_drive_url:
        return self.url_result(google_drive_url, 'GoogleDrive')
    mobj = re.search(('<iframe[^>]+src="(?:https?:)?(?P<url>%s)"' % UDNEmbedIE._PROTOCOL_RELATIVE_VALID_URL), webpage)
    if (mobj is not None):
        return self.url_result(compat_urlparse.urljoin(url, mobj.group('url')), 'UDNEmbed')
    senate_isvp_url = SenateISVPIE._search_iframe_url(webpage)
    if senate_isvp_url:
        return self.url_result(senate_isvp_url, 'SenateISVP')
    onionstudios_url = OnionStudiosIE._extract_url(webpage)
    if onionstudios_url:
        return self.url_result(onionstudios_url)
    viewlift_url = ViewLiftEmbedIE._extract_url(webpage)
    if viewlift_url:
        return self.url_result(viewlift_url)
    jwplatform_urls = JWPlatformIE._extract_urls(webpage)
    if jwplatform_urls:
        return self.playlist_from_matches(jwplatform_urls, video_id, video_title, ie=JWPlatformIE.ie_key())
    digiteka_url = DigitekaIE._extract_url(webpage)
    if digiteka_url:
        return self.url_result(self._proto_relative_url(digiteka_url), DigitekaIE.ie_key())
    arkena_url = ArkenaIE._extract_url(webpage)
    if arkena_url:
        return self.url_result(arkena_url, ArkenaIE.ie_key())
    piksel_url = PikselIE._extract_url(webpage)
    if piksel_url:
        return self.url_result(piksel_url, PikselIE.ie_key())
    limelight_urls = LimelightBaseIE._extract_urls(webpage, url)
    if limelight_urls:
        return self.playlist_result(limelight_urls, video_id, video_title, video_description)
    anvato_urls = AnvatoIE._extract_urls(self, webpage, video_id)
    if anvato_urls:
        return self.playlist_result(anvato_urls, video_id, video_title, video_description)
    mobj = re.search('<iframe[^>]+src=[\\\'"]((?:https?:)?//video\\.tv\\.adobe\\.com/v/\\d+[^"]+)[\\\'"]', webpage)
    if (mobj is not None):
        return self.url_result(self._proto_relative_url(unescapeHTML(mobj.group(1))), 'AdobeTVVideo')
    mobj = re.search('<iframe[^>]+src=[\\\'"]((?:https?:)?//(?:www\\.)?vine\\.co/v/[^/]+/embed/(?:simple|postcard))', webpage)
    if (mobj is not None):
        return self.url_result(self._proto_relative_url(unescapeHTML(mobj.group(1))), 'Vine')
    mobj = re.search('<iframe[^>]+src=(["\\\'])(?P<url>(?:https?:)?//(?:www\\.)?vod-platform\\.net/[eE]mbed/.+?)\\1', webpage)
    if (mobj is not None):
        return self.url_result(self._proto_relative_url(unescapeHTML(mobj.group('url'))), 'VODPlatform')
    mobj = re.search('(?x)<iframe[^>]+src=(["\\\'])(?P<url>(?:https?:)?//(?:www\\.)?admin\\.mangomolo\\.com/analytics/index\\.php/customers/embed/\n                (?:\n                    video\\?.*?\\bid=(?P<video_id>\\d+)|\n                    index\\?.*?\\bchannelid=(?P<channel_id>(?:[A-Za-z0-9+/=]|%2B|%2F|%3D)+)\n                ).+?)\\1', webpage)
    if (mobj is not None):
        info = {
            '_type': 'url_transparent',
            'url': self._proto_relative_url(unescapeHTML(mobj.group('url'))),
            'title': video_title,
            'description': video_description,
            'thumbnail': video_thumbnail,
            'uploader': video_uploader,
        }
        video_id = mobj.group('video_id')
        if video_id:
            info.update({
                'ie_key': 'MangomoloVideo',
                'id': video_id,
            })
        else:
            info.update({
                'ie_key': 'MangomoloLive',
                'id': mobj.group('channel_id'),
            })
        return info
    instagram_embed_url = InstagramIE._extract_embed_url(webpage)
    if (instagram_embed_url is not None):
        return self.url_result(self._proto_relative_url(instagram_embed_url), InstagramIE.ie_key())
    liveleak_urls = LiveLeakIE._extract_urls(webpage)
    if liveleak_urls:
        return self.playlist_from_matches(liveleak_urls, video_id, video_title)
    threeqsdn_url = ThreeQSDNIE._extract_url(webpage)
    if threeqsdn_url:
        return {
            '_type': 'url_transparent',
            'ie_key': ThreeQSDNIE.ie_key(),
            'url': self._proto_relative_url(threeqsdn_url),
            'title': video_title,
            'description': video_description,
            'thumbnail': video_thumbnail,
            'uploader': video_uploader,
        }
    vbox7_url = Vbox7IE._extract_url(webpage)
    if vbox7_url:
        return self.url_result(vbox7_url, Vbox7IE.ie_key())
    dbtv_urls = DBTVIE._extract_urls(webpage)
    if dbtv_urls:
        return self.playlist_from_matches(dbtv_urls, video_id, video_title, ie=DBTVIE.ie_key())
    videa_urls = VideaIE._extract_urls(webpage)
    if videa_urls:
        return self.playlist_from_matches(videa_urls, video_id, video_title, ie=VideaIE.ie_key())
    twentymin_urls = TwentyMinutenIE._extract_urls(webpage)
    if twentymin_urls:
        return self.playlist_from_matches(twentymin_urls, video_id, video_title, ie=TwentyMinutenIE.ie_key())
    openload_urls = OpenloadIE._extract_urls(webpage)
    if openload_urls:
        return self.playlist_from_matches(openload_urls, video_id, video_title, ie=OpenloadIE.ie_key())
    videopress_urls = VideoPressIE._extract_urls(webpage)
    if videopress_urls:
        return self.playlist_from_matches(videopress_urls, video_id, video_title, ie=VideoPressIE.ie_key())
    rutube_urls = RutubeIE._extract_urls(webpage)
    if rutube_urls:
        return self.playlist_from_matches(rutube_urls, video_id, video_title, ie=RutubeIE.ie_key())
    wapo_urls = WashingtonPostIE._extract_urls(webpage)
    if wapo_urls:
        return self.playlist_from_matches(wapo_urls, video_id, video_title, ie=WashingtonPostIE.ie_key())
    mediaset_urls = MediasetIE._extract_urls(webpage)
    if mediaset_urls:
        return self.playlist_from_matches(mediaset_urls, video_id, video_title, ie=MediasetIE.ie_key())
    joj_urls = JojIE._extract_urls(webpage)
    if joj_urls:
        return self.playlist_from_matches(joj_urls, video_id, video_title, ie=JojIE.ie_key())
    mpfn_urls = MegaphoneIE._extract_urls(webpage)
    if mpfn_urls:
        return self.playlist_from_matches(mpfn_urls, video_id, video_title, ie=MegaphoneIE.ie_key())
    vzaar_urls = VzaarIE._extract_urls(webpage)
    if vzaar_urls:
        return self.playlist_from_matches(vzaar_urls, video_id, video_title, ie=VzaarIE.ie_key())
    channel9_urls = Channel9IE._extract_urls(webpage)
    if channel9_urls:
        return self.playlist_from_matches(channel9_urls, video_id, video_title, ie=Channel9IE.ie_key())
    vshare_urls = VShareIE._extract_urls(webpage)
    if vshare_urls:
        return self.playlist_from_matches(vshare_urls, video_id, video_title, ie=VShareIE.ie_key())
    mediasite_urls = MediasiteIE._extract_urls(webpage)
    if mediasite_urls:
        entries = [self.url_result(smuggle_url(compat_urlparse.urljoin(url, mediasite_url), {
            'UrlReferrer': url,
        }), ie=MediasiteIE.ie_key()) for mediasite_url in mediasite_urls]
        return self.playlist_result(entries, video_id, video_title)
    springboardplatform_urls = SpringboardPlatformIE._extract_urls(webpage)
    if springboardplatform_urls:
        return self.playlist_from_matches(springboardplatform_urls, video_id, video_title, ie=SpringboardPlatformIE.ie_key())
    yapfiles_urls = YapFilesIE._extract_urls(webpage)
    if yapfiles_urls:
        return self.playlist_from_matches(yapfiles_urls, video_id, video_title, ie=YapFilesIE.ie_key())
    vice_urls = ViceIE._extract_urls(webpage)
    if vice_urls:
        return self.playlist_from_matches(vice_urls, video_id, video_title, ie=ViceIE.ie_key())
    xfileshare_urls = XFileShareIE._extract_urls(webpage)
    if xfileshare_urls:
        return self.playlist_from_matches(xfileshare_urls, video_id, video_title, ie=XFileShareIE.ie_key())

    def merge_dicts(dict1, dict2):
        merged = {
            
        }
        for (k, v) in dict1.items():
            if (v is not None):
                merged[k] = v
        for (k, v) in dict2.items():
            if (v is None):
                continue
            if ((k not in merged) or (isinstance(v, compat_str) and v and isinstance(merged[k], compat_str) and (not merged[k]))):
                merged[k] = v
        return merged
    entries = self._parse_html5_media_entries(url, webpage, video_id, m3u8_id='hls')
    if entries:
        if (len(entries) == 1):
            entries[0].update({
                'id': video_id,
                'title': video_title,
            })
        else:
            for (num, entry) in enumerate(entries, start=1):
                entry.update({
                    'id': ('%s-%s' % (video_id, num)),
                    'title': ('%s (%d)' % (video_title, num)),
                })
        for entry in entries:
            self._sort_formats(entry['formats'])
        return self.playlist_result(entries, video_id, video_title)
    jwplayer_data = self._find_jwplayer_data(webpage, video_id, transform_source=js_to_json)
    if jwplayer_data:
        info = self._parse_jwplayer_data(jwplayer_data, video_id, require_title=False, base_url=url)
        return merge_dicts(info, info_dict)
    mobj = re.search('(?s)\\bvideojs\\s*\\(.+?\\.src\\s*\\(\\s*((?:\\[.+?\\]|{.+?}))\\s*\\)\\s*;', webpage)
    if (mobj is not None):
        sources = (self._parse_json(mobj.group(1), video_id, transform_source=js_to_json, fatal=False) or [])
        if (not isinstance(sources, list)):
            sources = [sources]
        formats = []
        for source in sources:
            src = source.get('src')
            if ((not src) or (not isinstance(src, compat_str))):
                continue
            src = compat_urlparse.urljoin(url, src)
            src_type = source.get('type')
            if isinstance(src_type, compat_str):
                src_type = src_type.lower()
            ext = determine_ext(src).lower()
            if (src_type == 'video/youtube'):
                return self.url_result(src, YoutubeIE.ie_key())
            if ((src_type == 'application/dash+xml') or (ext == 'mpd')):
                formats.extend(self._extract_mpd_formats(src, video_id, mpd_id='dash', fatal=False))
            elif ((src_type == 'application/x-mpegurl') or (ext == 'm3u8')):
                formats.extend(self._extract_m3u8_formats(src, video_id, 'mp4', entry_protocol='m3u8_native', m3u8_id='hls', fatal=False))
            else:
                formats.append({
                    'url': src,
                    'ext': ((mimetype2ext(src_type) or ext) if (ext in KNOWN_EXTENSIONS) else 'mp4'),
                })
        if formats:
            self._sort_formats(formats)
            info_dict['formats'] = formats
            return info_dict
    json_ld = self._search_json_ld(webpage, video_id, default={
        
    }, expected_type='VideoObject')
    if json_ld.get('url'):
        return merge_dicts(json_ld, info_dict)

    def check_video(vurl):
        if YoutubeIE.suitable(vurl):
            return True
        if RtmpIE.suitable(vurl):
            return True
        vpath = compat_urlparse.urlparse(vurl).path
        vext = determine_ext(vpath)
        return (('.' in vpath) and (vext not in ('swf', 'png', 'jpg', 'srt', 'sbv', 'sub', 'vtt', 'ttml', 'js', 'xml')))

    def filter_video(urls):
        return list(filter(check_video, urls))
    found = filter_video(re.findall('flashvars: [\\\'"](?:.*&)?file=(http[^\\\'"&]*)', webpage))
    if (not found):
        found = filter_video(re.findall('(?sx)\n                (?:\n                    jw_plugins|\n                    JWPlayerOptions|\n                    jwplayer\\s*\\(\\s*["\'][^\'"]+["\']\\s*\\)\\s*\\.setup\n                )\n                .*?\n                [\'"]?file[\'"]?\\s*:\\s*["\\\'](.*?)["\\\']', webpage))
    if (not found):
        found = filter_video(re.findall('[^A-Za-z0-9]?(?:file|source)=(http[^\\\'"&]*)', webpage))
    if (not found):
        found = filter_video(re.findall('[^A-Za-z0-9]?(?:file|video_url)["\\\']?:\\s*["\\\'](http(?![^\\\'"]+\\.[0-9]+[\\\'"])[^\\\'"]+)["\\\']', webpage))
    if (not found):
        found = filter_video(re.findall('(?xs)\n                flowplayer\\("[^"]+",\\s*\n                    \\{[^}]+?\\}\\s*,\n                    \\s*\\{[^}]+? ["\']?clip["\']?\\s*:\\s*\\{\\s*\n                        ["\']?url["\']?\\s*:\\s*["\']([^"\']+)["\']\n            ', webpage))
    if (not found):
        found = re.findall("cinerama\\.embedPlayer\\(\\s*\\'[^']+\\',\\s*'([^']+)'", webpage)
    if (not found):
        found = filter_video(re.findall('<meta (?:property|name)="twitter:player:stream" (?:content|value)="(.+?)"', webpage))
    if (not found):
        m_video_type = re.findall('<meta.*?property="og:video:type".*?content="video/(.*?)"', webpage)
        if (m_video_type is not None):
            found = filter_video(re.findall('<meta.*?property="og:video".*?content="(.*?)"', webpage))
    if (not found):
        REDIRECT_REGEX = '[0-9]{,2};\\s*(?:URL|url)=\\\'?([^\\\'"]+)'
        found = re.search(('(?i)<meta\\s+(?=(?:[a-z-]+="[^"]+"\\s+)*http-equiv="refresh")(?:[a-z-]+="[^"]+"\\s+)*?content="%s' % REDIRECT_REGEX), webpage)
        if (not found):
            refresh_header = head_response.headers.get('Refresh')
            if refresh_header:
                if ((sys.version_info < (3, 0)) and isinstance(refresh_header, str)):
                    refresh_header = refresh_header.decode('iso-8859-1')
                found = re.search(REDIRECT_REGEX, refresh_header)
        if found:
            new_url = compat_urlparse.urljoin(url, unescapeHTML(found.group(1)))
            if (new_url != url):
                self.report_following_redirect(new_url)
                return {
                    '_type': 'url',
                    'url': new_url,
                }
            else:
                found = None
    if (not found):
        embed_url = self._html_search_meta('twitter:player', webpage, default=None)
        if (embed_url and (embed_url != url)):
            return self.url_result(embed_url)
    if (not found):
        raise UnsupportedError(url)
    entries = []
    for video_url in orderedSet(found):
        video_url = unescapeHTML(video_url)
        video_url = video_url.replace('\\/', '/')
        video_url = compat_urlparse.urljoin(url, video_url)
        video_id = compat_urllib_parse_unquote(os.path.basename(video_url))
        if YoutubeIE.suitable(video_url):
            entries.append(self.url_result(video_url, 'Youtube'))
            continue
        video_id = os.path.splitext(video_id)[0]
        entry_info_dict = {
            'id': video_id,
            'uploader': video_uploader,
            'title': video_title,
            'age_limit': age_limit,
        }
        if RtmpIE.suitable(video_url):
            entry_info_dict.update({
                '_type': 'url_transparent',
                'ie_key': RtmpIE.ie_key(),
                'url': video_url,
            })
            entries.append(entry_info_dict)
            continue
        ext = determine_ext(video_url)
        if (ext == 'smil'):
            entry_info_dict['formats'] = self._extract_smil_formats(video_url, video_id)
        elif (ext == 'xspf'):
            return self.playlist_result(self._extract_xspf_playlist(video_url, video_id), video_id)
        elif (ext == 'm3u8'):
            entry_info_dict['formats'] = self._extract_m3u8_formats(video_url, video_id, ext='mp4')
        elif (ext == 'mpd'):
            entry_info_dict['formats'] = self._extract_mpd_formats(video_url, video_id)
        elif (ext == 'f4m'):
            entry_info_dict['formats'] = self._extract_f4m_formats(video_url, video_id)
        elif (re.search('(?i)\\.(?:ism|smil)/manifest', video_url) and (video_url != url)):
            entry_info_dict = self.url_result(smuggle_url(video_url, {
                'to_generic': True,
            }), GenericIE.ie_key())
        else:
            entry_info_dict['url'] = video_url
        if entry_info_dict.get('formats'):
            self._sort_formats(entry_info_dict['formats'])
        entries.append(entry_info_dict)
    if (len(entries) == 1):
        return entries[0]
    else:
        for (num, e) in enumerate(entries, start=1):
            if (e.get('title') is not None):
                e['title'] = ('%s (%d)' % (e['title'], num))
        return {
            '_type': 'playlist',
            'entries': entries,
        }
