def select_on_queryset(self, queryset):
    '\n        This method runs either prefetch_related or select_related on the queryset\n        to improve indexing speed of the relation.\n\n        It decides which method to call based on the number of related objects:\n         - single (eg ForeignKey, OneToOne), it runs select_related\n         - multiple (eg ManyToMany, reverse ForeignKey) it runs prefetch_related\n        '
    try:
        field = self.get_field(queryset.model)
    except FieldDoesNotExist:
        return queryset
    if isinstance(field, RelatedField):
        if (field.many_to_one or field.one_to_one):
            queryset = queryset.select_related(self.field_name)
        elif (field.one_to_many or field.many_to_many):
            queryset = queryset.prefetch_related(self.field_name)
    elif isinstance(field, ForeignObjectRel):
        if isinstance(field, OneToOneRel):
            queryset = queryset.select_related(self.field_name)
        else:
            queryset = queryset.prefetch_related(self.field_name)
    return queryset