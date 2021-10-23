

def process_info(self, info_dict):
    'Process a single resolved IE result.'
    assert (info_dict.get('_type', 'video') == 'video')
    max_downloads = self.params.get('max_downloads')
    if (max_downloads is not None):
        if (self._num_downloads >= int(max_downloads)):
            raise MaxDownloadsReached()
    info_dict['fulltitle'] = info_dict['title']
    if (len(info_dict['title']) > 200):
        info_dict['title'] = (info_dict['title'][:197] + '...')
    if ('format' not in info_dict):
        info_dict['format'] = info_dict['ext']
    reason = self._match_entry(info_dict, incomplete=False)
    if (reason is not None):
        self.to_screen(('[download] ' + reason))
        return
    self._num_downloads += 1
    info_dict['_filename'] = filename = self.prepare_filename(info_dict)
    if self.params.get('forcetitle', False):
        self.to_stdout(info_dict['fulltitle'])
    if self.params.get('forceid', False):
        self.to_stdout(info_dict['id'])
    if self.params.get('forceurl', False):
        if (info_dict.get('requested_formats') is not None):
            for f in info_dict['requested_formats']:
                self.to_stdout((f['url'] + f.get('play_path', '')))
        else:
            self.to_stdout((info_dict['url'] + info_dict.get('play_path', '')))
    if (self.params.get('forcethumbnail', False) and (info_dict.get('thumbnail') is not None)):
        self.to_stdout(info_dict['thumbnail'])
    if (self.params.get('forcedescription', False) and (info_dict.get('description') is not None)):
        self.to_stdout(info_dict['description'])
    if (self.params.get('forcefilename', False) and (filename is not None)):
        self.to_stdout(filename)
    if (self.params.get('forceduration', False) and (info_dict.get('duration') is not None)):
        self.to_stdout(formatSeconds(info_dict['duration']))
    if self.params.get('forceformat', False):
        self.to_stdout(info_dict['format'])
    if self.params.get('forcejson', False):
        self.to_stdout(json.dumps(info_dict))
    if self.params.get('simulate', False):
        return
    if (filename is None):
        return
    try:
        dn = os.path.dirname(sanitize_path(encodeFilename(filename)))
        if (dn and (not os.path.exists(dn))):
            os.makedirs(dn)
    except (OSError, IOError) as err:
        self.report_error(('unable to create directory ' + error_to_compat_str(err)))
        return
    if self.params.get('writedescription', False):
        descfn = replace_extension(filename, 'description', info_dict.get('ext'))
        if (self.params.get('nooverwrites', False) and os.path.exists(encodeFilename(descfn))):
            self.to_screen('[info] Video description is already present')
        elif (info_dict.get('description') is None):
            self.report_warning("There's no description to write.")
        else:
            try:
                self.to_screen(('[info] Writing video description to: ' + descfn))
                with io.open(encodeFilename(descfn), 'w', encoding='utf-8') as descfile:
                    descfile.write(info_dict['description'])
            except (OSError, IOError):
                self.report_error(('Cannot write description file ' + descfn))
                return
    if self.params.get('writeannotations', False):
        annofn = replace_extension(filename, 'annotations.xml', info_dict.get('ext'))
        if (self.params.get('nooverwrites', False) and os.path.exists(encodeFilename(annofn))):
            self.to_screen('[info] Video annotations are already present')
        else:
            try:
                self.to_screen(('[info] Writing video annotations to: ' + annofn))
                with io.open(encodeFilename(annofn), 'w', encoding='utf-8') as annofile:
                    annofile.write(info_dict['annotations'])
            except (KeyError, TypeError):
                self.report_warning('There are no annotations to write.')
            except (OSError, IOError):
                self.report_error(('Cannot write annotations file: ' + annofn))
                return
    subtitles_are_requested = any([self.params.get('writesubtitles', False), self.params.get('writeautomaticsub')])
    if (subtitles_are_requested and info_dict.get('requested_subtitles')):
        subtitles = info_dict['requested_subtitles']
        ie = self.get_info_extractor(info_dict['extractor_key'])
        for (sub_lang, sub_info) in subtitles.items():
            sub_format = sub_info['ext']
            if (sub_info.get('data') is not None):
                sub_data = sub_info['data']
            else:
                try:
                    sub_data = ie._download_webpage(sub_info['url'], info_dict['id'], note=False)
                except ExtractorError as err:
                    self.report_warning(('Unable to download subtitle for "%s": %s' % (sub_lang, error_to_compat_str(err.cause))))
                    continue
            try:
                sub_filename = subtitles_filename(filename, sub_lang, sub_format)
                if (self.params.get('nooverwrites', False) and os.path.exists(encodeFilename(sub_filename))):
                    self.to_screen(('[info] Video subtitle %s.%s is already_present' % (sub_lang, sub_format)))
                else:
                    self.to_screen(('[info] Writing video subtitles to: ' + sub_filename))
                    with io.open(encodeFilename(sub_filename), 'w', encoding='utf-8', newline='') as subfile:
                        subfile.write(sub_data)
            except (OSError, IOError):
                self.report_error(('Cannot write subtitles file ' + sub_filename))
                return
    if self.params.get('writeinfojson', False):
        infofn = replace_extension(filename, 'info.json', info_dict.get('ext'))
        if (self.params.get('nooverwrites', False) and os.path.exists(encodeFilename(infofn))):
            self.to_screen('[info] Video description metadata is already present')
        else:
            self.to_screen(('[info] Writing video description metadata as JSON to: ' + infofn))
            try:
                write_json_file(self.filter_requested_info(info_dict), infofn)
            except (OSError, IOError):
                self.report_error(('Cannot write metadata to JSON file ' + infofn))
                return
    self._write_thumbnails(info_dict, filename)
    if (not self.params.get('skip_download', False)):
        try:

            def dl(name, info):
                fd = get_suitable_downloader(info, self.params)(self, self.params)
                for ph in self._progress_hooks:
                    fd.add_progress_hook(ph)
                if self.params.get('verbose'):
                    self.to_stdout(('[debug] Invoking downloader on %r' % info.get('url')))
                return fd.download(name, info)
            if (info_dict.get('requested_formats') is not None):
                downloaded = []
                success = True
                merger = FFmpegMergerPP(self)
                if (not merger.available):
                    postprocessors = []
                    self.report_warning("You have requested multiple formats but ffmpeg or avconv are not installed. The formats won't be merged.")
                else:
                    postprocessors = [merger]

                def compatible_formats(formats):
                    (video, audio) = formats
                    (video_ext, audio_ext) = (audio.get('ext'), video.get('ext'))
                    if (video_ext and audio_ext):
                        COMPATIBLE_EXTS = (('mp3', 'mp4', 'm4a', 'm4p', 'm4b', 'm4r', 'm4v'), 'webm')
                        for exts in COMPATIBLE_EXTS:
                            if ((video_ext in exts) and (audio_ext in exts)):
                                return True
                    return False
                filename_real_ext = os.path.splitext(filename)[1][1:]
                filename_wo_ext = (os.path.splitext(filename)[0] if (filename_real_ext == info_dict['ext']) else filename)
                requested_formats = info_dict['requested_formats']
                if ((self.params.get('merge_output_format') is None) and (not compatible_formats(requested_formats))):
                    info_dict['ext'] = 'mkv'
                    self.report_warning('Requested formats are incompatible for merge and will be merged into mkv.')
                filename = ('%s.%s' % (filename_wo_ext, info_dict['ext']))
                if os.path.exists(encodeFilename(filename)):
                    self.to_screen(('[download] %s has already been downloaded and merged' % filename))
                else:
                    for f in requested_formats:
                        new_info = dict(info_dict)
                        new_info.update(f)
                        fname = self.prepare_filename(new_info)
                        fname = prepend_extension(fname, ('f%s' % f['format_id']), new_info['ext'])
                        downloaded.append(fname)
                        partial_success = dl(fname, new_info)
                        success = (success and partial_success)
                    info_dict['__postprocessors'] = postprocessors
                    info_dict['__files_to_merge'] = downloaded
            else:
                success = dl(filename, info_dict)
        except (compat_urllib_error.URLError, compat_http_client.HTTPException, socket.error) as err:
            self.report_error(('unable to download video data: %s' % error_to_compat_str(err)))
            return
        except (OSError, IOError) as err:
            raise UnavailableVideoError(err)
        except (ContentTooShortError,) as err:
            self.report_error(('content too short (expected %s bytes and served %s)' % (err.expected, err.downloaded)))
            return
        if (success and (filename != '-')):
            fixup_policy = self.params.get('fixup')
            if (fixup_policy is None):
                fixup_policy = 'detect_or_warn'
            INSTALL_FFMPEG_MESSAGE = 'Install ffmpeg or avconv to fix this automatically.'
            stretched_ratio = info_dict.get('stretched_ratio')
            if ((stretched_ratio is not None) and (stretched_ratio != 1)):
                if (fixup_policy == 'warn'):
                    self.report_warning(('%s: Non-uniform pixel ratio (%s)' % (info_dict['id'], stretched_ratio)))
                elif (fixup_policy == 'detect_or_warn'):
                    stretched_pp = FFmpegFixupStretchedPP(self)
                    if stretched_pp.available:
                        info_dict.setdefault('__postprocessors', [])
                        info_dict['__postprocessors'].append(stretched_pp)
                    else:
                        self.report_warning(('%s: Non-uniform pixel ratio (%s). %s' % (info_dict['id'], stretched_ratio, INSTALL_FFMPEG_MESSAGE)))
                else:
                    assert (fixup_policy in ('ignore', 'never'))
            if ((info_dict.get('requested_formats') is None) and (info_dict.get('container') == 'm4a_dash')):
                if (fixup_policy == 'warn'):
                    self.report_warning(('%s: writing DASH m4a. Only some players support this container.' % info_dict['id']))
                elif (fixup_policy == 'detect_or_warn'):
                    fixup_pp = FFmpegFixupM4aPP(self)
                    if fixup_pp.available:
                        info_dict.setdefault('__postprocessors', [])
                        info_dict['__postprocessors'].append(fixup_pp)
                    else:
                        self.report_warning(('%s: writing DASH m4a. Only some players support this container. %s' % (info_dict['id'], INSTALL_FFMPEG_MESSAGE)))
                else:
                    assert (fixup_policy in ('ignore', 'never'))
            if ((info_dict.get('protocol') == 'm3u8_native') or ((info_dict.get('protocol') == 'm3u8') and self.params.get('hls_prefer_native'))):
                if (fixup_policy == 'warn'):
                    self.report_warning(('%s: malformated aac bitstream.' % info_dict['id']))
                elif (fixup_policy == 'detect_or_warn'):
                    fixup_pp = FFmpegFixupM3u8PP(self)
                    if fixup_pp.available:
                        info_dict.setdefault('__postprocessors', [])
                        info_dict['__postprocessors'].append(fixup_pp)
                    else:
                        self.report_warning(('%s: malformated aac bitstream. %s' % (info_dict['id'], INSTALL_FFMPEG_MESSAGE)))
                else:
                    assert (fixup_policy in ('ignore', 'never'))
            try:
                self.post_process(filename, info_dict)
            except PostProcessingError as err:
                self.report_error(('postprocessing: %s' % str(err)))
                return
            self.record_download_archive(info_dict)
