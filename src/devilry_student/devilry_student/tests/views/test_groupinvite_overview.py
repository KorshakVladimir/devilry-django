from django.test import TestCase
from django.core.urlresolvers import reverse

from devilry.apps.core.models import GroupInvite
from devilry_developer.testhelpers.soupselect import cssFind
from devilry_developer.testhelpers.soupselect import cssGet
from devilry_developer.testhelpers.soupselect import prettyhtml
from devilry_developer.testhelpers.corebuilder import PeriodBuilder
from devilry_developer.testhelpers.corebuilder import UserBuilder


class TestGroupInviteOverviewView(TestCase):
    def setUp(self):
        self.testuser = UserBuilder('testuser').user

    def _getas(self, id, user, *args, **kwargs):
        self.client.login(username=user.username, password='test')
        url = reverse('devilry_student_groupinvite_overview', kwargs={'group_id': id})
        return self.client.get(url, *args, **kwargs)

    def _postas(self, id, user, *args, **kwargs):
        self.client.login(username=user.username, password='test')
        url = reverse('devilry_student_groupinvite_overview', kwargs={'group_id': id})
        return self.client.post(url, *args, **kwargs)

    def test_render(self):
        group = PeriodBuilder.quickadd_ducku_duck1010_active()\
            .add_assignment('assignment1')\
            .add_group(students=[self.testuser]).group
        response = self._getas(group.id, self.testuser)
        self.assertEquals(response.status_code, 200)
        html = response.content
        self.assertEquals(cssGet(html, 'h1').text.strip(), 'Project groupduck1010.active.assignment1')

    def test_only_if_student(self):
        group = PeriodBuilder.quickadd_ducku_duck1010_active()\
            .add_assignment('assignment1')\
            .add_group().group
        response = self._getas(group.id, self.testuser)
        self.assertEquals(response.status_code, 404)

    def test_send_invite_to_selectlist(self):
        UserBuilder('ignoreduser')
        alreadyingroupuser1 = UserBuilder('alreadyingroupuser1').user
        alreadyingroupuser2 = UserBuilder('alreadyingroupuser2').user
        hasinviteuser = UserBuilder('hasinviteuser').user
        matchuser1 = UserBuilder('matchuser1').user
        matchuser2 = UserBuilder('matchuser2', full_name='Match User Two').user

        group = PeriodBuilder.quickadd_ducku_duck1010_active()\
            .add_relatedstudents(
                alreadyingroupuser1, alreadyingroupuser2, hasinviteuser,
                matchuser1, matchuser2)\
            .add_assignment('assignment1', students_can_create_groups=True)\
            .add_group(students=[alreadyingroupuser1, alreadyingroupuser2]).group
        group.groupinvite_set.create(
            sent_by=alreadyingroupuser1,
            sent_to=hasinviteuser)

        html = self._getas(group.id, alreadyingroupuser1).content
        send_to_options = [e.text.strip() for e in cssFind(html, '#id_sent_to option')]
        self.assertEquals(send_to_options, ['', 'matchuser1', 'Match User Two'])


    def test_send_to_post(self):
        inviteuser = UserBuilder('inviteuser').user
        group = PeriodBuilder.quickadd_ducku_duck1010_active()\
            .add_relatedstudents(self.testuser, inviteuser)\
            .add_assignment('assignment1', students_can_create_groups=True)\
            .add_group(students=[self.testuser]).group

        self.assertEquals(GroupInvite.objects.count(), 0)
        response = self._postas(group.id, self.testuser, {
            'sent_to': inviteuser.id
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(GroupInvite.objects.count(), 1)
        invite = GroupInvite.objects.all()[0]
        self.assertEquals(invite.sent_by, self.testuser)
        self.assertEquals(invite.sent_to, inviteuser)
        self.assertEquals(invite.accepted, None)

    def test_send_to_post_notrelated(self):
        inviteuser = UserBuilder('inviteuser').user
        group = PeriodBuilder.quickadd_ducku_duck1010_active()\
            .add_relatedstudents(self.testuser)\
            .add_assignment('assignment1', students_can_create_groups=True)\
            .add_group(students=[self.testuser]).group

        self.assertEquals(GroupInvite.objects.count(), 0)
        response = self._postas(group.id, self.testuser, {
            'sent_to': inviteuser.id
        })
        self.assertEquals(response.status_code, 200)
        self.assertIn(
            'Select a valid choice. {} is not one of the available choices.'.format(inviteuser.id),
            response.content)