def run(self, terms, variables=None, **kwargs):
    validate_certs = kwargs.get('validate_certs', True)
    split_lines = kwargs.get('split_lines', True)
    use_proxy = kwargs.get('use_proxy', True)
    ret = []
    for term in terms:
        display.vvvv(('url lookup connecting to %s' % term))
        try:
            response = open_url(term, validate_certs=validate_certs, use_proxy=use_proxy)
        except HTTPError as e:
            raise AnsibleError(('Received HTTP error for %s : %s' % (term, str(e))))
        except URLError as e:
            raise AnsibleError(('Failed lookup url for %s : %s' % (term, str(e))))
        except SSLValidationError as e:
            raise AnsibleError(("Error validating the server's certificate for %s: %s" % (term, str(e))))
        except ConnectionError as e:
            raise AnsibleError(('Error connecting to %s: %s' % (term, str(e))))
        if split_lines:
            for line in response.read().splitlines():
                ret.append(to_text(line))
        else:
            ret.append(to_text(response.read()))
    return ret