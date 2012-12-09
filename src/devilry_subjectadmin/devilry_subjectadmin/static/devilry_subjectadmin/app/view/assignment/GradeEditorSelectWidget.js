Ext.define('devilry_subjectadmin.view.assignment.GradeEditorSelectWidget', {
    extend: 'devilry_extjsextras.ContainerWithEditTitle',
    alias: 'widget.gradeeditorselect-widget',
    cls: 'devilry_subjectadmin_gradeeditorselect_widget',
    title: gettext('Grading system'),

    requires: [
        'devilry_extjsextras.MarkupMoreInfoBox'
    ],

    //buttonSuffix: '<i class="icon-chevron-right"></i>',
    buttonSuffix: '<span class="forward-indicator"></span>',

    body: {
        xtype: 'markupmoreinfobox',
        moreCls: 'alert alert-info',
        tpl: [
            '<tpl if="loading">',
                '<p><small>{loading}</small></p>',
            '<tpl else>',
                '<p class="muted">',
                    '{title}',
                    ' <small>{MORE_BUTTON}</small>',
                '</p>',
                '<div {MORE_ATTRS}>',
                    gettext('Click the edit button for more information about grading systems and your current grading system.'),
                '</div>',
                '<tpl if="isMissingConfig">',
                    '<div class="alert alert-error">',
                        gettext('Missing grading system config. You have to configure this grading system before any feeback may be provided on this assignment.'),
                    '</div>',
                '</tpl>',
            '</tpl>'
        ],
        data: {
            loading: gettext('Loading') + ' ...'
        }
    }
});
