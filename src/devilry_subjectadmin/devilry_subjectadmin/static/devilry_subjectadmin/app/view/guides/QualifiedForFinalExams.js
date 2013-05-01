Ext.define('devilry_subjectadmin.view.guides.QualifiedForFinalExams', {
    extend: 'Ext.container.Container',
    alias: 'widget.guide-qualifiedforfinalexams',

    /**
     * @cfg {devilry_subjectadmin.controller.GuideSystem} [guideSystem]
     */

    layout: 'card',
    defaults: {
        xtype: 'box'
    },
    items: [{
        itemId: 'loading',
        html: ['<p>', gettext('Loading') + ' ...', '</p>'].join('')
    }, {
        itemId: 'dashboard',
        tpl: [
            '<p>',
                gettext('Select an active {subject_term} from the list at the top of the left side of this page.'),
            '</p>',
            '<p><small>',
                gettext('For {subjects_term} where you only have admin rights for selected assignments, those assignments will be listed. If you only have assignments in your list, you do not have the required rights to select students that qualify for final exams.'),
            '</small></p>'
        ],
        data: {
            subject_term: gettext('subject'),
            subjects_term: gettext('subjects')
        }
    }, {
        itemId: 'period',
        tpl: [
            '<p>',
                gettext('Click the <em>Qualified for final exams</em>-link near the bottom of the page.'),
            '</p>',
            '<p>',
                gettext('On the next page this guide will disappear, and a new guide will begin. If you, or another admin, have already selected students that qualify for final exams, you will see the results of that selection instead of beginning a new guide.')
        ],
        data: {
        }
    }]
});
