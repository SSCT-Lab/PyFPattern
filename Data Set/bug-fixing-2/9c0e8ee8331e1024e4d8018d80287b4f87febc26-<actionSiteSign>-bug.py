

def actionSiteSign(self, to, privatekey=None, inner_path='content.json', remove_missing_optional=False, update_changed_files=False, response_ok=True):
    self.log.debug(('Signing: %s' % inner_path))
    site = self.site
    extend = {
        
    }
    file_info = site.content_manager.getFileInfo(inner_path)
    if (not inner_path.endswith('content.json')):
        if (not file_info):
            raise Exception(('Invalid content.json file: %s' % inner_path))
        inner_path = file_info['content_inner_path']
    is_user_content = (file_info and (('cert_signers' in file_info) or ('cert_signers_pattern' in file_info)))
    if (is_user_content and (privatekey is None)):
        cert = self.user.getCert(self.site.address)
        extend['cert_auth_type'] = cert['auth_type']
        extend['cert_user_id'] = self.user.getCertUserId(site.address)
        extend['cert_sign'] = cert['cert_sign']
        self.log.debug(('Extending content.json with cert %s' % extend['cert_user_id']))
    if (not self.hasFilePermission(inner_path)):
        self.log.error("SiteSign error: you don't own this site & site owner doesn't allow you to do so.")
        return self.response(to, {
            'error': 'Forbidden, you can only modify your own sites',
        })
    if (privatekey == 'stored'):
        privatekey = self.user.getSiteData(self.site.address).get('privatekey')
    if (not privatekey):
        privatekey = self.user.getAuthPrivatekey(self.site.address)
    site.content_manager.loadContent(inner_path, add_bad_files=False, force=True)
    try:
        site.content_manager.sign(inner_path, privatekey, extend=extend, update_changed_files=update_changed_files, remove_missing_optional=remove_missing_optional)
    except (VerifyError, SignError) as err:
        self.cmd('notification', ['error', (_['Content signing failed'] + ('<br><small>%s</small>' % err))])
        self.response(to, {
            'error': ('Site sign failed: %s' % err),
        })
        self.log.error(('Site sign failed: %s: %s' % (inner_path, Debug.formatException(err))))
        return
    except Exception as err:
        self.cmd('notification', ['error', (_['Content signing error'] + ('<br><small>%s</small>' % Debug.formatException(err)))])
        self.response(to, {
            'error': ('Site sign error: %s' % Debug.formatException(err)),
        })
        self.log.error(('Site sign error: %s: %s' % (inner_path, Debug.formatException(err))))
        return
    site.content_manager.loadContent(inner_path, add_bad_files=False)
    if update_changed_files:
        self.site.updateWebsocket(file_done=inner_path)
    if response_ok:
        self.response(to, 'ok')
    else:
        return inner_path
