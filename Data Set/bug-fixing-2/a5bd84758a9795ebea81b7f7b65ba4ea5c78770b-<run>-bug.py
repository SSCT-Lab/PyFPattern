

def run(self, terms, variables=None, **kwargs):
    self.set_options(direct=kwargs)
    ret = []
    for term in terms:
        display.vvvv(('url lookup connecting to %s' % term))
        try:
            response = open_url(term, validate_certs=self.get_option('validate_certs'), use_proxy=self.get_option('use_proxy'), url_username=self.get_option('url_username'), url_password=self.get_option('url_password'))
        except HTTPError as e:
            raise AnsibleError(('Received HTTP error for %s : %s' % (term, to_native(e))))
        except URLError as e:
            raise AnsibleError(('Failed lookup url for %s : %s' % (term, to_native(e))))
        except SSLValidationError as e:
            raise AnsibleError(("Error validating the server's certificate for %s: %s" % (term, to_native(e))))
        except ConnectionError as e:
            raise AnsibleError(('Error connecting to %s: %s' % (term, to_native(e))))
        if self.get_option('split_lines'):
            for line in response.read().splitlines():
                ret.append(to_text(line))
        else:
            ret.append(to_text(response.read()))
    return ret
