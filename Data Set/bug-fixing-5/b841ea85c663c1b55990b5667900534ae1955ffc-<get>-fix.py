def get(self, request, organization=None):
    if ((request.GET.get('show') == 'all') and is_active_superuser(request) and request.access.has_permission('broadcasts.admin')):
        queryset = Broadcast.objects.all().order_by('-date_added')
    else:
        queryset = Broadcast.objects.filter((Q(date_expires__isnull=True) | Q(date_expires__gt=timezone.now())), is_active=True).order_by('-date_added')
    query = request.GET.get('query')
    if query:
        tokens = tokenize_query(query)
        for (key, value) in six.iteritems(tokens):
            if (key == 'query'):
                value = ' '.join(value)
                queryset = queryset.filter(((Q(title__icontains=value) | Q(message__icontains=value)) | Q(link__icontains=value)))
            elif (key == 'id'):
                queryset = queryset.filter(id__in=value)
            elif (key == 'link'):
                queryset = queryset.filter(in_icontains('link', value))
            elif (key == 'status'):
                filters = []
                for v in value:
                    v = v.lower()
                    if (v == 'active'):
                        filters.append((Q(date_expires__isnull=True, is_active=True) | Q(date_expires__gt=timezone.now(), is_active=True)))
                    elif (v == 'inactive'):
                        filters.append((Q(date_expires__lt=timezone.now()) | Q(is_active=False)))
                    else:
                        queryset = queryset.none()
                if filters:
                    queryset = queryset.filter(six.moves.reduce(or_, filters))
            else:
                queryset = queryset.none()
    if organization:
        data = self._secondary_filtering(request, organization, queryset)
        return self.respond(self._serialize_objects(data, request))
    sort_by = request.GET.get('sortBy')
    if (sort_by == 'expires'):
        order_by = '-date_expires'
        paginator_cls = DateTimePaginator
    else:
        order_by = '-date_added'
        paginator_cls = DateTimePaginator
    return self.paginate(request=request, queryset=queryset, order_by=order_by, on_results=(lambda x: self._serialize_objects(x, request)), paginator_cls=paginator_cls)