from django_filters import rest_framework as filters
from notes.models import Note


class ArchiveFilter(filters.FilterSet):
    """
    ArchiveFilter : Filters the queryset based on the
                    archive boolean variable
    """

    archive = filters.BooleanFilter(method="filter_is_archive")

    class Meta:
        model: Note
        fields = ("archive",)

    def filter_is_archive(queryset):
        queryset = queryset.filter(archive="True")
        return queryset
