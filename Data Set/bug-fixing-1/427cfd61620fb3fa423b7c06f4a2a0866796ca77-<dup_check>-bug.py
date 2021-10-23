

def dup_check(module, iam, name, new_name, cert, orig_cert_names, orig_cert_bodies, dup_ok):
    update = False
    if any(((ct in orig_cert_names) for ct in [name, new_name])):
        for i_name in [name, new_name]:
            if (i_name is None):
                continue
            if (cert is not None):
                try:
                    c_index = orig_cert_names.index(i_name)
                except NameError:
                    continue
                else:
                    if (orig_cert_bodies[c_index] == cert):
                        update = True
                        break
                    elif (orig_cert_bodies[c_index] != cert):
                        module.fail_json(changed=False, msg=('A cert with the name %s already exists and has a different certificate body associated with it. Certificates cannot have the same name' % i_name))
            else:
                update = True
                break
    elif ((cert in orig_cert_bodies) and (not dup_ok)):
        for (crt_name, crt_body) in zip(orig_cert_names, orig_cert_bodies):
            if (crt_body == cert):
                module.fail_json(changed=False, msg=('This certificate already exists under the name %s' % crt_name))
    return update
