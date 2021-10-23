def dup_check(module, iam, name, new_name, cert, orig_cert_names, orig_cert_bodies, dup_ok):
    update = False
    names_lower = [n.lower() for n in [name, new_name]]
    orig_cert_names_lower = [ocn.lower() for ocn in orig_cert_names]
    if any(((ct in orig_cert_names_lower) for ct in names_lower)):
        for i_name in names_lower:
            if (i_name is None):
                continue
            if (cert is not None):
                try:
                    c_index = orig_cert_names_lower.index(i_name)
                except NameError:
                    continue
                else:
                    slug_cert = cert.replace('\r', '')
                    slug_orig_cert_bodies = orig_cert_bodies[c_index].replace('\r', '')
                    if (slug_orig_cert_bodies == slug_cert):
                        update = True
                        break
                    elif slug_cert.startswith(slug_orig_cert_bodies):
                        update = True
                        break
                    elif (slug_orig_cert_bodies != slug_cert):
                        module.fail_json(changed=False, msg=('A cert with the name %s already exists and has a different certificate body associated with it. Certificates cannot have the same name' % i_name))
            else:
                update = True
                break
    elif ((cert in orig_cert_bodies) and (not dup_ok)):
        for (crt_name, crt_body) in zip(orig_cert_names, orig_cert_bodies):
            if (crt_body == cert):
                module.fail_json(changed=False, msg=('This certificate already exists under the name %s' % crt_name))
    return update