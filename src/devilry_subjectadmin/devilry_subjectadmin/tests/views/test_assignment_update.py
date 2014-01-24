from django.test import TestCase
from django.core.urlresolvers import reverse

from devilry_developer.testhelpers.soupselect import cssFind
from devilry_developer.testhelpers.soupselect import cssGet
from devilry_developer.testhelpers.soupselect import prettyhtml
from devilry_developer.testhelpers.corebuilder import PeriodBuilder
from devilry_developer.testhelpers.corebuilder import UserBuilder
from devilry_developer.testhelpers.datebuilder import DateTimeBuilder
from devilry_subjectadmin.tests.utils import isoformat_datetime


class TestAssignmentUpdateView(TestCase):
    def setUp(self):
        self.testuser = UserBuilder('testuser').user

    def _getas(self, id, user, *args, **kwargs):
        self.client.login(username=user.username, password='test')
        url = reverse('devilry_subjectadmin_assignment_update', kwargs={'id': id})
        return self.client.get(url, *args, **kwargs)

    def _postas(self, id, user, *args, **kwargs):
        self.client.login(username=user.username, password='test')
        url = reverse('devilry_subjectadmin_assignment_update', kwargs={'id': id})
        return self.client.post(url, *args, **kwargs)

    def test_render(self):
        periodbuilder = PeriodBuilder.quickadd_ducku_duck1010_active()\
            .add_admins(self.testuser)

        publishing_time = DateTimeBuilder.now().plus(days=10)
        assignment1builder = periodbuilder.add_assignment('assignment1',
            long_name='Assignment One',
            anonymous=True,
            publishing_time=publishing_time,
            deadline_handling=1)
        response = self._getas(assignment1builder.assignment.id, self.testuser)
        self.assertEquals(response.status_code, 200)
        html = response.content
        self.assertEquals(cssGet(html, 'input[name=long_name]')['value'], 'Assignment One')
        self.assertEquals(cssGet(html, 'input[name=deadline_handling]')['value'], '1')
        self.assertEquals(cssGet(html, 'input[name=publishing_time]')['value'],
            isoformat_datetime(publishing_time))
        self.assertEquals(cssGet(html, 'input[name=short_name]')['value'], 'assignment1')

    def test_update(self):
        periodbuilder = PeriodBuilder.quickadd_ducku_duck1010_active()\
            .add_admins(self.testuser)

        publishing_time = DateTimeBuilder.now().plus(days=10)
        assignment1builder = periodbuilder.add_assignment('assignment1',
            long_name='Assignment One',
            anonymous=True,
            publishing_time=publishing_time,
            deadline_handling=1,
            max_points=10, # Should not be touched by the update
            passing_grade_min_points=8 # Should not be touched by the update
        )

        new_publishing_time = DateTimeBuilder.now().plus(days=20).replace(second=0, microsecond=0, tzinfo=None)
        response = self._postas(assignment1builder.assignment.id, self.testuser, {
            'long_name': 'Test One',
            'short_name': 'test1',
            'anonymous': '',
            'publishing_time': isoformat_datetime(new_publishing_time),
            'deadline_handling': 0
        })
        self.assertEquals(response.status_code, 302)
        assignment1builder.reload_from_db()
        assignment = assignment1builder.assignment
        self.assertEquals(assignment.long_name, 'Test One')
        self.assertEquals(assignment.short_name, 'test1')
        self.assertFalse(assignment.anonymous)
        self.assertEquals(assignment.publishing_time, new_publishing_time)
        self.assertEquals(assignment.deadline_handling, 0)
        self.assertEquals(assignment.max_points, 10)
        self.assertEquals(assignment.passing_grade_min_points, 8)