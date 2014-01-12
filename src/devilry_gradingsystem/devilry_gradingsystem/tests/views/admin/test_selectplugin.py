from mock import patch
from django.core.urlresolvers import reverse
from django.test import TestCase

from devilry_developer.testhelpers.corebuilder import PeriodBuilder
from devilry_developer.testhelpers.corebuilder import UserBuilder
from devilry_developer.testhelpers.soupselect import cssGet
from devilry_developer.testhelpers.soupselect import cssFind
from devilry_gradingsystem.pluginregistry import GradingSystemPluginRegistry

from .base import AdminViewTestMixin
from .base import MockApprovedPluginApi
from .base import MockPointsPluginApi
from .base import MockRequiresConfigurationPluginApi



class TestSelectPluginView(TestCase, AdminViewTestMixin):

    def setUp(self):
        self.admin1 = UserBuilder('admin1').user
        self.assignmentbuilder = PeriodBuilder.quickadd_ducku_duck1010_active()\
            .add_assignment('assignment1')\
            .add_admins(self.admin1)
        self.url = reverse('devilry_gradingsystem_admin_selectplugin', kwargs={
            'assignmentid': self.assignmentbuilder.assignment.id,
        })

    def test_get_not_admin_404_with_pluginselected(self):
        nobody = UserBuilder('nobody').user
        myregistry = GradingSystemPluginRegistry()
        myregistry.add(MockPointsPluginApi)
        with patch('devilry_gradingsystem.views.admin.selectplugin.gradingsystempluginregistry', myregistry):
            self.assertIn(MockPointsPluginApi.id, myregistry)
            response = self.get_as(nobody, {
                'selected_plugin_id': MockPointsPluginApi.id
            })
            self.assertEquals(response.status_code, 404)

    def test_render(self):
        myregistry = GradingSystemPluginRegistry()
        myregistry.add(MockPointsPluginApi)
        myregistry.add(MockApprovedPluginApi)
        with patch('devilry_gradingsystem.views.admin.selectplugin.gradingsystempluginregistry', myregistry):
            response = self.get_as(self.admin1)
            self.assertEquals(response.status_code, 200)
            html = response.content
            self.assertEquals(cssGet(html, '.page-header h1').text.strip(),
                'How would you like to configure the plugin?')
            self.assertEquals(len(cssFind(html, '.devilry_gradingsystem_selectplugin_box')), 2)

    def test_next_page_requires_configuration(self):
        myregistry = GradingSystemPluginRegistry()
        myregistry.add(MockRequiresConfigurationPluginApi)
        with patch('devilry_gradingsystem.views.admin.selectplugin.gradingsystempluginregistry', myregistry):
            response = self.get_as(self.admin1, {
                'selected_plugin_id': MockRequiresConfigurationPluginApi.id
            })
            self.assertEquals(response.status_code, 302)
            self.assertEquals(response["Location"],
                'http://testserver/mock/requiresconfiguration/configure/{}'.format(
                    self.assignmentbuilder.assignment.id))

    def test_next_page_no_configuration_required(self):
        myregistry = GradingSystemPluginRegistry()
        myregistry.add(MockPointsPluginApi)
        with patch('devilry_gradingsystem.views.admin.selectplugin.gradingsystempluginregistry', myregistry):
            response = self.get_as(self.admin1, {
                'selected_plugin_id': MockPointsPluginApi.id
            })
            self.assertEquals(response.status_code, 302)
            self.assertTrue(response["Location"].endswith(
                reverse('devilry_gradingsystem_admin_setmaxpoints', kwargs={
                    'assignmentid': self.assignmentbuilder.assignment.id})))
