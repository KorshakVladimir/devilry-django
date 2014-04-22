from django.test import TestCase
from django.core.urlresolvers import reverse

from devilry_developer.testhelpers.corebuilder import PeriodBuilder
from devilry_developer.testhelpers.corebuilder import SubjectBuilder
from devilry_developer.testhelpers.corebuilder import NodeBuilder
from devilry_developer.testhelpers.corebuilder import UserBuilder
from devilry_developer.testhelpers.soupselect import cssFind
from devilry_developer.testhelpers.soupselect import cssGet
from devilry_developer.testhelpers.soupselect import cssExists
from devilry_developer.testhelpers.login import LoginTestCaseMixin



class TestFrontpage(TestCase, LoginTestCaseMixin):
    def setUp(self):
        self.url = reverse('devilry_frontpage')
        self.testuser = UserBuilder('testuser')

    def test_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

    def test_authenticated(self):
        response = self.get_as(self.testuser.user, self.url)
        self.assertEquals(response.status_code, 200)
    
    def test_roleselect_student(self):
        PeriodBuilder.quickadd_ducku_duck1010_active()\
            .add_assignment('week1')\
            .add_group(students=[self.testuser.user])
        html = self.get_as(self.testuser.user, self.url).content
        self.assertEquals(len(cssFind(html, '#devilry_frontpage_roleselect a')), 1)
        self.assertTrue(cssExists(html, '#devilry_frontpage_roleselect_student'))

    def test_roleselect_examiner(self):
        PeriodBuilder.quickadd_ducku_duck1010_active()\
            .add_assignment('week1')\
            .add_group(examiners=[self.testuser.user])
        html = self.get_as(self.testuser.user, self.url).content
        self.assertEquals(len(cssFind(html, '#devilry_frontpage_roleselect a')), 1)
        self.assertTrue(cssExists(html, '#devilry_frontpage_roleselect_examiner'))

    def test_roleselect_subjectadmin(self):
        SubjectBuilder.quickadd_ducku_duck1010().add_admins(self.testuser.user)
        html = self.get_as(self.testuser.user, self.url).content
        self.assertEquals(len(cssFind(html, '#devilry_frontpage_roleselect a')), 1)
        self.assertTrue(cssExists(html, '#devilry_frontpage_roleselect_subjectadmin'))

    def test_roleselect_nodeadmin(self):
        NodeBuilder('univ').add_admins(self.testuser.user)
        html = self.get_as(self.testuser.user, self.url).content
        self.assertEquals(len(cssFind(html, '#devilry_frontpage_roleselect a')), 1)
        self.assertTrue(cssExists(html, '#devilry_frontpage_roleselect_nodeadmin'))

    def test_roleselect_superuser(self):
        self.testuser.update(is_superuser=True, is_staff=True)
        html = self.get_as(self.testuser.user, self.url).content
        self.assertEquals(len(cssFind(html, '#devilry_frontpage_roleselect a')), 2)
        self.assertTrue(cssExists(html, '#devilry_frontpage_roleselect_nodeadmin'))
        self.assertTrue(cssExists(html, '#devilry_frontpage_roleselect_superuser'))

    def test_roleselect_superuser_not_staff(self):
        self.testuser.update(is_superuser=True, is_staff=False)
        html = self.get_as(self.testuser.user, self.url).content
        self.assertEquals(len(cssFind(html, '#devilry_frontpage_roleselect a')), 1)
        self.assertTrue(cssExists(html, '#devilry_frontpage_roleselect_nodeadmin'))
        self.assertFalse(cssExists(html, '#devilry_frontpage_roleselect_superuser'))


    def test_helplinks(self):
        html = self.get_as(self.testuser.user, self.url).content
        self.assertTrue(cssExists(html, '#devilry_frontpage_helplinks'))
        self.assertEquals(
            cssGet(html, '#devilry_frontpage_helplinks ul li a').text.strip(),
            'Official Devilry documentation')

    def test_languageselect(self):
        self.testuser.update_profile(
            languagecode='en'
        )
        with self.settings(LANGUAGES=[('en', 'English'), ('nb', 'Norwegian')]):
            html = self.get_as(self.testuser.user, self.url).content
            self.assertTrue(cssExists(html,
                '#devilry_frontpage_languageselect #devilry_change_language_form'))
            self.assertEquals(
                cssGet(html, '#devilry_change_language_form option[value="en"]')['selected'],
                'selected')

    def test_languageselect_no_current_language(self):
        with self.settings(
                LANGUAGES=[('en', 'English'), ('nb', 'Norwegian')],
                LANGUAGE_CODE='nb'):
            html = self.get_as(self.testuser.user, self.url).content
            self.assertTrue(cssExists(html,
                '#devilry_frontpage_languageselect #devilry_change_language_form'))
            self.assertEquals(
                cssGet(html, '#devilry_change_language_form option[value="nb"]')['selected'],
                'selected')