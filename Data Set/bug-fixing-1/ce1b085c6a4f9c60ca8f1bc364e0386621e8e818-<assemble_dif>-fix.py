

@instrumented_task(name='sentry.tasks.assemble.assemble_dif', queue='assemble')
def assemble_dif(project_id, name, checksum, chunks, **kwargs):
    '\n    Assembles uploaded chunks into a ``ProjectDebugFile``.\n    '
    from sentry.models import debugfile, Project, BadDif
    from sentry.reprocessing import bump_reprocessing_revision
    with configure_scope() as scope:
        scope.set_tag('project', project_id)
    project = Project.objects.filter(id=project_id).get()
    set_assemble_status(AssembleTask.DIF, project.id, checksum, ChunkFileState.ASSEMBLING)
    rv = assemble_file(AssembleTask.DIF, project, name, checksum, chunks, file_type='project.dif')
    if (rv is None):
        return
    (file, temp_file) = rv
    delete_file = True
    try:
        with temp_file:
            try:
                result = debugfile.detect_dif_from_path(temp_file.name, name=name)
            except BadDif as e:
                set_assemble_status(AssembleTask.DIF, project.id, checksum, ChunkFileState.ERROR, detail=e.args[0])
                return
            if (len(result) != 1):
                detail = ('Object contains %s architectures (1 expected)' % len(result))
                set_assemble_status(AssembleTask.DIF, project.id, checksum, ChunkFileState.ERROR, detail=detail)
                return
            (dif, created) = debugfile.create_dif_from_id(project, result[0], file=file)
            delete_file = False
            if created:
                bump_reprocessing_revision(project)
    except BaseException:
        set_assemble_status(AssembleTask.DIF, project.id, checksum, ChunkFileState.ERROR, detail='internal server error')
        logger.error('failed to assemble dif', exc_info=True)
    else:
        set_assemble_status(AssembleTask.DIF, project.id, checksum, ChunkFileState.OK, detail=serialize(dif))
    finally:
        if delete_file:
            file.delete()
