

def _parse_mpd_formats(self, mpd_doc, mpd_id=None, mpd_base_url='', formats_dict={
    
}, mpd_url=None):
    '\n        Parse formats from MPD manifest.\n        References:\n         1. MPEG-DASH Standard, ISO/IEC 23009-1:2014(E),\n            http://standards.iso.org/ittf/PubliclyAvailableStandards/c065274_ISO_IEC_23009-1_2014.zip\n         2. https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP\n        '
    if (mpd_doc.get('type') == 'dynamic'):
        return []
    namespace = self._search_regex('(?i)^{([^}]+)?}MPD$', mpd_doc.tag, 'namespace', default=None)

    def _add_ns(path):
        return self._xpath_ns(path, namespace)

    def is_drm_protected(element):
        return (element.find(_add_ns('ContentProtection')) is not None)

    def extract_multisegment_info(element, ms_parent_info):
        ms_info = ms_parent_info.copy()

        def extract_common(source):
            segment_timeline = source.find(_add_ns('SegmentTimeline'))
            if (segment_timeline is not None):
                s_e = segment_timeline.findall(_add_ns('S'))
                if s_e:
                    ms_info['total_number'] = 0
                    ms_info['s'] = []
                    for s in s_e:
                        r = int(s.get('r', 0))
                        ms_info['total_number'] += (1 + r)
                        ms_info['s'].append({
                            't': int(s.get('t', 0)),
                            'd': int(s.attrib['d']),
                            'r': r,
                        })
            start_number = source.get('startNumber')
            if start_number:
                ms_info['start_number'] = int(start_number)
            timescale = source.get('timescale')
            if timescale:
                ms_info['timescale'] = int(timescale)
            segment_duration = source.get('duration')
            if segment_duration:
                ms_info['segment_duration'] = float(segment_duration)

        def extract_Initialization(source):
            initialization = source.find(_add_ns('Initialization'))
            if (initialization is not None):
                ms_info['initialization_url'] = initialization.attrib['sourceURL']
        segment_list = element.find(_add_ns('SegmentList'))
        if (segment_list is not None):
            extract_common(segment_list)
            extract_Initialization(segment_list)
            segment_urls_e = segment_list.findall(_add_ns('SegmentURL'))
            if segment_urls_e:
                ms_info['segment_urls'] = [segment.attrib['media'] for segment in segment_urls_e]
        else:
            segment_template = element.find(_add_ns('SegmentTemplate'))
            if (segment_template is not None):
                extract_common(segment_template)
                media = segment_template.get('media')
                if media:
                    ms_info['media'] = media
                initialization = segment_template.get('initialization')
                if initialization:
                    ms_info['initialization'] = initialization
                else:
                    extract_Initialization(segment_template)
        return ms_info
    mpd_duration = parse_duration(mpd_doc.get('mediaPresentationDuration'))
    formats = []
    for period in mpd_doc.findall(_add_ns('Period')):
        period_duration = (parse_duration(period.get('duration')) or mpd_duration)
        period_ms_info = extract_multisegment_info(period, {
            'start_number': 1,
            'timescale': 1,
        })
        for adaptation_set in period.findall(_add_ns('AdaptationSet')):
            if is_drm_protected(adaptation_set):
                continue
            adaption_set_ms_info = extract_multisegment_info(adaptation_set, period_ms_info)
            for representation in adaptation_set.findall(_add_ns('Representation')):
                if is_drm_protected(representation):
                    continue
                representation_attrib = adaptation_set.attrib.copy()
                representation_attrib.update(representation.attrib)
                mime_type = representation_attrib['mimeType']
                content_type = mime_type.split('/')[0]
                if (content_type == 'text'):
                    pass
                elif (content_type in ('video', 'audio')):
                    base_url = ''
                    for element in (representation, adaptation_set, period, mpd_doc):
                        base_url_e = element.find(_add_ns('BaseURL'))
                        if (base_url_e is not None):
                            base_url = (base_url_e.text + base_url)
                            if re.match('^https?://', base_url):
                                break
                    if (mpd_base_url and (not re.match('^https?://', base_url))):
                        if ((not mpd_base_url.endswith('/')) and (not base_url.startswith('/'))):
                            mpd_base_url += '/'
                        base_url = (mpd_base_url + base_url)
                    representation_id = representation_attrib.get('id')
                    lang = representation_attrib.get('lang')
                    url_el = representation.find(_add_ns('BaseURL'))
                    filesize = int_or_none((url_el.attrib.get('{http://youtube.com/yt/2012/10/10}contentLength') if (url_el is not None) else None))
                    bandwidth = int_or_none(representation_attrib.get('bandwidth'))
                    f = {
                        'format_id': (('%s-%s' % (mpd_id, representation_id)) if mpd_id else representation_id),
                        'url': base_url,
                        'manifest_url': mpd_url,
                        'ext': mimetype2ext(mime_type),
                        'width': int_or_none(representation_attrib.get('width')),
                        'height': int_or_none(representation_attrib.get('height')),
                        'tbr': float_or_none(bandwidth, 1000),
                        'asr': int_or_none(representation_attrib.get('audioSamplingRate')),
                        'fps': int_or_none(representation_attrib.get('frameRate')),
                        'language': (lang if (lang not in ('mul', 'und', 'zxx', 'mis')) else None),
                        'format_note': ('DASH %s' % content_type),
                        'filesize': filesize,
                    }
                    f.update(parse_codecs(representation_attrib.get('codecs')))
                    representation_ms_info = extract_multisegment_info(representation, adaption_set_ms_info)

                    def prepare_template(template_name, identifiers):
                        t = representation_ms_info[template_name]
                        t = t.replace('$RepresentationID$', representation_id)
                        t = re.sub(('\\$(%s)\\$' % '|'.join(identifiers)), '%(\\1)d', t)
                        t = re.sub(('\\$(%s)%%([^$]+)\\$' % '|'.join(identifiers)), '%(\\1)\\2', t)
                        t.replace('$$', '$')
                        return t
                    if ('initialization' in representation_ms_info):
                        initialization_template = prepare_template('initialization', ('Bandwidth',))
                        representation_ms_info['initialization_url'] = (initialization_template % {
                            'Bandwidth': bandwidth,
                        })

                    def location_key(location):
                        return ('url' if re.match('^https?://', location) else 'path')
                    if (('segment_urls' not in representation_ms_info) and ('media' in representation_ms_info)):
                        media_template = prepare_template('media', ('Number', 'Bandwidth', 'Time'))
                        media_location_key = location_key(media_template)
                        if (('%(Number' in media_template) and ('s' not in representation_ms_info)):
                            segment_duration = None
                            if (('total_number' not in representation_ms_info) and 'segment_duration'):
                                segment_duration = float_or_none(representation_ms_info['segment_duration'], representation_ms_info['timescale'])
                                representation_ms_info['total_number'] = int(math.ceil((float(period_duration) / segment_duration)))
                            representation_ms_info['fragments'] = [{
                                media_location_key: (media_template % {
                                    'Number': segment_number,
                                    'Bandwidth': bandwidth,
                                }),
                                'duration': segment_duration,
                            } for segment_number in range(representation_ms_info['start_number'], (representation_ms_info['total_number'] + representation_ms_info['start_number']))]
                        else:
                            representation_ms_info['fragments'] = []
                            segment_time = 0
                            segment_d = None
                            segment_number = representation_ms_info['start_number']

                            def add_segment_url():
                                segment_url = (media_template % {
                                    'Time': segment_time,
                                    'Bandwidth': bandwidth,
                                    'Number': segment_number,
                                })
                                representation_ms_info['fragments'].append({
                                    media_location_key: segment_url,
                                    'duration': float_or_none(segment_d, representation_ms_info['timescale']),
                                })
                            for (num, s) in enumerate(representation_ms_info['s']):
                                segment_time = (s.get('t') or segment_time)
                                segment_d = s['d']
                                add_segment_url()
                                segment_number += 1
                                for r in range(s.get('r', 0)):
                                    segment_time += segment_d
                                    add_segment_url()
                                    segment_number += 1
                                segment_time += segment_d
                    elif (('segment_urls' in representation_ms_info) and ('s' in representation_ms_info)):
                        fragments = []
                        segment_index = 0
                        timescale = representation_ms_info['timescale']
                        for s in representation_ms_info['s']:
                            duration = float_or_none(s['d'], timescale)
                            for r in range((s.get('r', 0) + 1)):
                                segment_uri = representation_ms_info['segment_urls'][segment_index]
                                fragments.append({
                                    location_key(segment_uri): segment_uri,
                                    'duration': duration,
                                })
                                segment_index += 1
                        representation_ms_info['fragments'] = fragments
                    if ('fragments' in representation_ms_info):
                        f.update({
                            'fragment_base_url': base_url,
                            'fragments': [],
                            'protocol': 'http_dash_segments',
                        })
                        if ('initialization_url' in representation_ms_info):
                            initialization_url = representation_ms_info['initialization_url']
                            if (not f.get('url')):
                                f['url'] = initialization_url
                            f['fragments'].append({
                                location_key(initialization_url): initialization_url,
                            })
                        f['fragments'].extend(representation_ms_info['fragments'])
                    try:
                        existing_format = next((fo for fo in formats if (fo['format_id'] == representation_id)))
                    except StopIteration:
                        full_info = formats_dict.get(representation_id, {
                            
                        }).copy()
                        full_info.update(f)
                        formats.append(full_info)
                    else:
                        existing_format.update(f)
                else:
                    self.report_warning(('Unknown MIME type %s in DASH manifest' % mime_type))
    return formats
