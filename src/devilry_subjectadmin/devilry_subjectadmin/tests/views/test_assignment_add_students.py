from django.test import TestCase
from django.core.urlresolvers import reverse

from devilry_developer.testhelpers.soupselect import cssFind
from devilry_developer.testhelpers.soupselect import cssGet
from devilry_developer.testhelpers.soupselect import prettyhtml
from devilry_developer.testhelpers.corebuilder import PeriodBuilder
from devilry_developer.testhelpers.corebuilder import UserBuilder
from devilry_developer.testhelpers.datebuilder import DateTimeBuilder
from devilry_subjectadmin.tests.utils import isoformat_datetime


class TestAssignmentAddStudentsView(TestCase):
    def setUp(self):
        self.testuser = UserBuilder('testuser').user

    def _getas(self, id, user, *args, **kwargs):
        self.client.login(username=user.username, password='test')
        url = reverse('devilry_subjectadmin_assignment_add_students', kwargs={'id': id})
        return self.client.get(url, *args, **kwargs)

    def _postas(self, id, user, *args, **kwargs):
        self.client.login(username=user.username, password='test')
        url = reverse('devilry_subjectadmin_assignment_add_students', kwargs={'id': id})
        return self.client.post(url, *args, **kwargs)

    def test_only_admin(self):
        periodadmin = UserBuilder('periodadmin').user
        assignmentadmin = UserBuilder('assignmentadmin').user
        nobody = UserBuilder('nobody').user
        superuser = UserBuilder('superuser', is_superuser=True).user
        periodbuilder = PeriodBuilder.quickadd_ducku_duck1010_active()\
            .add_admins(periodadmin)
        assignment1builder = periodbuilder.add_assignment('assignment1')\
            .add_admins(assignmentadmin)

        self.assertEquals(self._getas(assignment1builder.assignment.id, periodadmin).status_code, 200)
        self.assertEquals(self._getas(assignment1builder.assignment.id, assignmentadmin).status_code, 200)
        self.assertEquals(self._getas(assignment1builder.assignment.id, superuser).status_code, 200)
        self.assertEquals(self._getas(assignment1builder.assignment.id, nobody).status_code, 404)

    def test_render(self):
        periodbuilder = PeriodBuilder.quickadd_ducku_duck1010_active()\
            .add_admins(self.testuser)

        first_deadline = DateTimeBuilder.now().plus(days=10)
        assignment1builder = periodbuilder.add_assignment('assignment1',
            first_deadline=first_deadline)
        response = self._getas(assignment1builder.assignment.id, self.testuser)
        self.assertEquals(response.status_code, 200)
        html = response.content
        self.assertEquals(cssGet(html, 'input[name=first_deadline]')['value'],
            isoformat_datetime(first_deadline))

    def test_update(self):
        periodbuilder = PeriodBuilder.quickadd_ducku_duck1010_active()\
            .add_admins(self.testuser)

        first_deadline = DateTimeBuilder.now().plus(days=10)
        assignment1builder = periodbuilder.add_assignment('assignment1',
            first_deadline=first_deadline,
            max_points=8 # Should not be touched by the update
        )

        new_first_deadline = DateTimeBuilder.now().plus(days=20).replace(second=0, microsecond=0, tzinfo=None)
        response = self._postas(assignment1builder.assignment.id, self.testuser, {
            'first_deadline': isoformat_datetime(new_first_deadline)
        })
        self.assertEquals(response.status_code, 302)
        assignment1builder.reload_from_db()
        assignment = assignment1builder.assignment
        self.assertEquals(assignment.first_deadline, new_first_deadline)
        self.assertEquals(assignment.max_points, 8) # Unaffected?