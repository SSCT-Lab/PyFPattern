def _system_state_change(state, records, description, ttl, zone, recordset):
    if (state == 'present'):
        if (recordset is None):
            return True
        if ((records is not None) and (recordset['records'] != records)):
            return True
        if ((description is not None) and (recordset['description'] != description)):
            return True
        if ((ttl is not None) and (recordset['ttl'] != ttl)):
            return True
    if ((state == 'absent') and recordset):
        return True
    return False