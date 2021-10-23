def handle(self, **options):
    db = options['database']
    interactive = options['interactive']
    verbosity = options['verbosity']
    for app_config in apps.get_app_configs():
        (content_types, app_models) = get_contenttypes_and_models(app_config, db, ContentType)
        to_remove = [ct for (model_name, ct) in content_types.items() if (model_name not in app_models)]
        using = router.db_for_write(ContentType)
        if to_remove:
            if interactive:
                ct_info = []
                for ct in to_remove:
                    ct_info.append(('    - Content type for %s.%s' % (ct.app_label, ct.model)))
                    collector = NoFastDeleteCollector(using=using)
                    collector.collect([ct])
                    for (obj_type, objs) in collector.data.items():
                        if (objs == {ct}):
                            continue
                        ct_info.append(('    - %s %s object(s)' % (len(objs), obj_type._meta.label)))
                    content_type_display = '\n'.join(ct_info)
                self.stdout.write(("Some content types in your database are stale and can be deleted.\nAny objects that depend on these content types will also be deleted.\nThe content types and dependent objects that would be deleted are:\n\n%s\n\nThis list doesn't include any cascade deletions to data outside of Django's\nmodels (uncommon).\n\nAre you sure you want to delete these content types?\nIf you're unsure, answer 'no'.\n" % content_type_display))
                ok_to_delete = input("Type 'yes' to continue, or 'no' to cancel: ")
            else:
                ok_to_delete = False
            if (ok_to_delete == 'yes'):
                for ct in to_remove:
                    if (verbosity >= 2):
                        self.stdout.write(("Deleting stale content type '%s | %s'" % (ct.app_label, ct.model)))
                    ct.delete()
            elif (verbosity >= 2):
                self.stdout.write('Stale content types remain.')