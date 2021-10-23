

def check_migration_histories(histories, delete_ghosts=False, ignore_ghosts=False):
    "Checks that there's no 'ghost' migrations in the database."
    exists = SortedSet()
    ghosts = []
    for h in histories:
        try:
            m = h.get_migration()
            m.migration()
        except exceptions.UnknownMigration:
            ghosts.append(h)
        except ImproperlyConfigured:
            pass
        else:
            exists.add(m)
    if ghosts:
        if delete_ghosts:
            for h in ghosts:
                h.delete()
        elif (not ignore_ghosts):
            raise exceptions.GhostMigrations(ghosts)
    return exists
