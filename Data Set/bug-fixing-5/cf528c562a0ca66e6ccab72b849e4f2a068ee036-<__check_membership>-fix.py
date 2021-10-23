def __check_membership(self, src_role, dst_role):
    query = ("SELECT ARRAY(SELECT b.rolname FROM pg_catalog.pg_auth_members m JOIN pg_catalog.pg_roles b ON (m.roleid = b.oid) WHERE m.member = r.oid) FROM pg_catalog.pg_roles r WHERE r.rolname = '%s'" % dst_role)
    res = exec_sql(self, query, add_to_executed=False)
    membership = []
    if res:
        membership = res[0][0]
    if (not membership):
        return False
    if (src_role in membership):
        return True
    return False