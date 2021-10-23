@click.command()
@click.argument('dest', default='-', type=click.File('wb'))
@click.option('--silent', '-q', default=False, is_flag=True, help='Silence all debug output.')
@click.option('--indent', default=2, help='Number of spaces to indent for the JSON output. (default: 2)')
@click.option('--exclude', default=None, help='Models to exclude from export.', metavar='MODELS')
@configuration
def export(dest, silent, indent, exclude):
    'Exports core metadata for the Sentry installation.'
    if (exclude is None):
        exclude = ()
    else:
        exclude = exclude.lower().split(',')
    from django.core import serializers

    def yield_objects():
        for model in sort_dependencies():
            if ((not getattr(model, '__core__', True)) or (model.__name__.lower() in exclude) or model._meta.proxy):
                if (not silent):
                    click.echo(('>> Skipping model <%s>' % (model.__name__,)), err=True)
                continue
            queryset = model._base_manager.order_by(model._meta.pk.name)
            for obj in queryset.iterator():
                (yield obj)
    if (not silent):
        click.echo('>> Beginning export', err=True)
    serializers.serialize('json', yield_objects(), indent=indent, stream=dest, use_natural_foreign_keys=True)