from devilry.apps.core.testhelper import TestHelper

from .base import SubjectAdminSeleniumTestCase


class TestManageStudents(SubjectAdminSeleniumTestCase):
    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes='uni',
                            subjects=['sub'],
                            periods=['p1'],
                            assignments=['a1:admin(a1admin)'])

    def setUpStudentsBasic(self):
        self.testhelper.add_to_path('uni;sub.p1.a1.g1:candidate(student1)')
        self.testhelper.add_to_path('uni;sub.p1.a1.g2:candidate(student2)')
        self.testhelper.add_to_path('uni;sub.p1.a1.g3:candidate(student3)')

    def _setupStudentsFull(self):
        self.testhelper.add_to_path('uni;sub.p1.a1.g1:candidate(student1):examiner(examiner1).dl:ends(5)')
        self.testhelper.add_to_path('uni;sub.p1.a1.g2:candidate(student2):examiner(examiner1).dl:ends(5)')
        self.testhelper.add_to_path('uni;sub.p1.a1.g3:candidate(student3):examiner(examiner1).dl:ends(5)')
        self.testhelper.add_to_path('uni;sub.p1.a1.g4:candidate(student4):examiner(examiner1).dl:ends(5)')
        self.testhelper.add_to_path('uni;sub.p1.a1.g5:candidate(student5):examiner(examiner2).dl:ends(5)')
        self.testhelper.add_to_path('uni;sub.p1.a1.g6:candidate(student6):examiner(examiner2).dl:ends(5)')
        self.testhelper.add_to_path('uni;sub.p1.a1.g7:candidate(student7)')
        self.testhelper.add_to_path('uni;sub.p1.a1.g8:candidate(student8)')

        goodFile = {'good.py': ['print ', 'awesome']}
        okFile = {'ok.py': ['print ', 'meh']}
        badFile = {'bad.py': ['print ', 'bah']}

        self.testhelper.add_delivery('uni;sub.p1.a1.g1', badFile)
        self.testhelper.add_delivery('uni;sub.p1.a1.g1', okFile)
        self.testhelper.add_delivery('uni;sub.p1.a1.g1', goodFile)
        self.testhelper.add_delivery('uni;sub.p1.a1.g2', badFile)
        self.testhelper.add_delivery('uni;sub.p1.a1.g2', goodFile)
        self.testhelper.add_delivery('uni;sub.p1.a1.g3', okFile)
        self.testhelper.add_delivery('uni;sub.p1.a1.g4', badFile)
        self.testhelper.add_delivery('uni;sub.p1.a1.g5', badFile)
        self.testhelper.add_delivery('uni;sub.p1.a1.g6', badFile)

        goodVerdict = None
        okVerdict = {'grade': 'C', 'points': 85, 'is_passing_grade': True}
        badVerdict = {'grade': 'E', 'points': 60, 'is_passing_grade': True}
        failVerdict = {'grade': 'F', 'points': 30, 'is_passing_grade': False}

        self.testhelper.add_feedback('uni;sub.p1.a1.g1', verdict=goodVerdict)
        self.testhelper.add_feedback('uni;sub.p1.a1.g3', verdict=okVerdict)
        self.testhelper.add_feedback('uni;sub.p1.a1.g4', verdict=badVerdict)
        self.testhelper.add_feedback('uni;sub.p1.a1.g5', verdict=failVerdict)

    def _browseToManagestudentsAs(self, username, assignment):
        self.loginTo(username, '/assignment/{0}/@@manage-students/'.format(assignment.id))

    def test_listlength(self):
        self.setUpStudentsBasic()
        self._browseToManagestudentsAs('a1admin', self.testhelper.sub_p1_a1)
        self.waitForCssSelector('.devilry_subjectadmin_managestudentsoverview', timeout=20)

        self.waitForCssSelector('.devilry_subjectadmin_listofgroups')
        self.waitForCssSelector('.groupInfoWrapper')
        students=self.selenium.find_elements_by_css_selector('.groupInfoWrapper')
        self.assertEquals(len(students), 3)

    def test_listcontent(self):
        self._setupStudentsFull()
        self._browseToManagestudentsAs('a1admin', self.testhelper.sub_p1_a1)
        self.waitForCssSelector('.devilry_subjectadmin_managestudentsoverview', timeout=20)

        self.waitForCssSelector('.devilry_subjectadmin_listofgroups')
        self.waitForCssSelector('.groupInfoWrapper')

        ident=self.selenium.find_elements_by_css_selector('.groupInfoWrapper')
        self.assertIn('student1', ident[0].text)
        self.assertIn('student7', ident[6].text)
        self.assertIn('Passed (A)', ident[0].text)
        self.assertIn('Failed (F)', ident[4].text)

        stat=self.selenium.find_elements_by_css_selector('.metadataWrapper')
        self.assertIn('Closed', stat[0].text)
        self.assertIn('3 Deliveries', stat[0].text)

        self.assertIn('Open', stat[6].text)

    def _clickButton(self, parent, buttoncls):
        button = parent.find_element_by_css_selector('.{0} button'.format(buttoncls))
        button.click()

    def _clickLink(self, parent, buttoncls):
        button = parent.find_element_by_css_selector('.{0} a'.format(buttoncls))
        button.click()

    def _get_number_of_selected(self, lvl0_link_cls, *clickchain):
        """
        :param lvl0_link_cls: The css class of the link in the root of the selectMenu to click. We click this link first.
        :param lvl1_menu_cls: The css class of the first lvl2_menu_cls (the menu opened by clicking ``lvl0_link_cls``.
        """
        self._setupStudentsFull()
        self._browseToManagestudentsAs('a1admin', self.testhelper.sub_p1_a1)
        self.waitForCssSelector('.devilry_subjectadmin_managestudentsoverview', timeout=20)
        self.waitForCssSelector('.devilry_subjectadmin_listofgroups')
        self.waitForCssSelector('.groupInfoWrapper')
        self._clickButton(self.selenium, 'selectButton')
        selectMenu = self.waitForAndFindElementByCssSelector('.selectMenu')
        self._clickLink(selectMenu, lvl0_link_cls)

        for menucls, link_cls_or_index in clickchain:
            menu = self.waitForAndFindElementByCssSelector('.{0}'.format(menucls))
            if isinstance(link_cls_or_index, int):
                linkindex = link_cls_or_index
                links = menu.find_elements_by_css_selector('.x-menu-item')
                link = links[linkindex]
            else:
                linkcls = link_cls_or_index
                link = self.waitForAndFindElementByCssSelector('.{0}'.format(linkcls))
            link.find_element_by_css_selector('a').click()
        selected = self.selenium.find_elements_by_css_selector('.x-grid-row-selected')
        return len(selected)


    def test_select_by_status(self):
        count=self._get_number_of_selected('replaceSelectionButton',
                                           ('replaceSelectionMenu', 'byStatusButton'),
                                           ('byStatusMenu', 'selectStatusOpen'))
        self.assertEquals(count, 4)

    def test_select_by_feedback(self):
        count=self._get_number_of_selected('replaceSelectionButton',
                                           ('replaceSelectionMenu', 'byFeedbackButton'),
                                           ('byFeedbackMenu', 'selectGradePassed'))
        self.assertEquals(count, 3)

    def test_select_by_deliveries(self):
        count=self._get_number_of_selected('replaceSelectionButton',
                                           ('replaceSelectionMenu', 'byDeliveryNumButton'),
                                           ('byDeliveryMenu', 'selectHasDeliveries'))
        self.assertEquals(count, 6)

    def test_select_by_examiner(self):
        count=self._get_number_of_selected('replaceSelectionButton',
                                           ('replaceSelectionMenu', 'byExaminerButton'),
                                           ('byExaminerMenu', 'selectNoExaminer'))
        self.assertEquals(count, 2)

    def test_select_by_tag(self):
        count=self._get_number_of_selected('replaceSelectionButton',
                                           ('replaceSelectionMenu', 'byTagButton'),
                                           ('byTagMenu', 'selectNoTag'))
        self.assertEquals(count, 8)

    def test_select_by_specific_examiner(self):
        count=self._get_number_of_selected('replaceSelectionButton',
                                           ('replaceSelectionMenu', 'byExaminerButton'),
                                           ('byExaminerMenu', 'selectBySpecificExaminer'),
                                           ('devilry_subjectadmin_dynamicloadmenu', 0))
        self.assertEquals(count, 4)

    def test_select_by_specific_num_delivery(self):
        count=self._get_number_of_selected('replaceSelectionButton',
                                           ('replaceSelectionMenu', 'byDeliveryNumButton'),
                                           ('byDeliveryMenu', 'selectByDeliveryExactNum'),
                                           ('devilry_subjectadmin_dynamicloadmenu', 0))
        self.assertEquals(count, 2)

    def test_select_by_specific_feedback_grade(self):
        count=self._get_number_of_selected('replaceSelectionButton',
                                           ('replaceSelectionMenu', 'byFeedbackButton'),
                                           ('byFeedbackMenu', 'selectByFeedbackWithGrade'),
                                           ('devilry_subjectadmin_dynamicloadmenu', 0))
        self.assertEquals(count, 1)

    def test_select_by_specific_feedback_points(self):
        count=self._get_number_of_selected('replaceSelectionButton',
                                           ('replaceSelectionMenu', 'byFeedbackButton'),
                                           ('byFeedbackMenu', 'selectByFeedbackWithPoints'),
                                           ('devilry_subjectadmin_dynamicloadmenu', 0))
        self.assertEquals(count, 1)
