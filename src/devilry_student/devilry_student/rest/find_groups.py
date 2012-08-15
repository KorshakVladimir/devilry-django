from django.db.models.query import EmptyQuerySet
from django.db.models import Q
from djangorestframework.views import ListModelView
from djangorestframework.resources import ModelResource
from djangorestframework.permissions import IsAuthenticated

from devilry.apps.core.models import AssignmentGroup
from .helpers import GroupResourceHelpersMixin


class FindGroupsResource(ModelResource, GroupResourceHelpersMixin):
    fields = ('id', 'name', 'assignment', 'period', 'subject')
    model = AssignmentGroup

    def assignment(self, instance):
        return self.format_basenode(instance.parentnode)

    def period(self, instance):
        return self.format_basenode(instance.parentnode.parentnode)

    def subject(self, instance):
        return self.format_basenode(instance.parentnode.parentnode.parentnode)



class FindGroupsView(ListModelView):
    """
    Search for groups by the authenticated user.

    # GET

    ## Parameters
    Use the ``query`` parameter in the querystring to search for groups by:

    - Group name
    - Assignment (long and short name)
    - Period (long and short name)
    - Subject (long and short name)

    Uses case-ignore-contains search.


    ## Response
    List of objects with the following attributes:

    - ``id`` (int): Internal Devilry ID of the group. Is never ``null``.
    - ``name`` (string|null): The name of the group.
    - ``assignment`` (object): Information about the assignment.
    - ``period`` (object): Information about the period.
    - ``subject`` (object): Information about the subject.

    The response contains at most most 50 elements, and it is ordered by
    the publishing_time of the assignment (newest first).
    """
    permissions = (IsAuthenticated,)
    resource = FindGroupsResource

    def get_queryset(self):
        querystring = self.request.GET.get('query', '').strip()
        if not querystring:
            return EmptyQuerySet()
        qry = AssignmentGroup.published_where_is_candidate(self.request.user)
        qry = qry.filter(Q(name__icontains=querystring) |
                         # Assignment
                         Q(parentnode__short_name__icontains=querystring) |
                         Q(parentnode__long_name__icontains=querystring) |
                         # Period
                         Q(parentnode__parentnode__short_name__icontains=querystring) |
                         Q(parentnode__parentnode__long_name__icontains=querystring) |
                         # Subject
                         Q(parentnode__parentnode__parentnode__short_name__icontains=querystring) |
                         Q(parentnode__parentnode__parentnode__long_name__icontains=querystring))
        qry = qry.select_related('parentnode',
                                 'parentnode__parentnode',
                                 'parentnode__parentnode__parentnode')
        qry = qry.order_by('-parentnode__publishing_time')
        return qry[:50]
