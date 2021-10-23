def netconf_edit_config(m, xml, commit, retkwargs):
    if (':candidate' in m.server_capabilities):
        datastore = 'candidate'
    else:
        datastore = 'running'
    m.lock(target=datastore)
    try:
        if (':candidate' in m.server_capabilities):
            m.discard_changes()
        config_before = m.get_config(source=datastore)
        m.edit_config(target=datastore, config=xml)
        config_after = m.get_config(source=datastore)
        changed = (config_before.data_xml != config_after.data_xml)
        if (changed and commit and (':candidate' in m.server_capabilities)):
            if (':confirmed-commit' in m.server_capabilities):
                m.commit(confirmed=True)
                m.commit()
            else:
                m.commit()
        return changed
    finally:
        m.unlock(target=datastore)