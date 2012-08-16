Ext.define('devilry_student.view.dashboard.RecentFeedbacksGrid', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.recentfeedbacksgrid',
    cls: 'devilry_student_recentfeedbacksgrid',
    requires: [
        'devilry_extjsextras.DatetimeHelpers'
    ],

    frame: false,
    border: 0,
    hideHeaders: true,
    store: 'RecentFeedbacks',
    disableSelection: true,

    col1Tpl: [
        '<div><a href="#/group/{delivery.group.id}/{delivery.id}">',
            '{delivery.subject.short_name} - {delivery.assignment.short_name} - #{delivery.number}',
        '</a></div>',
        '<div>',
            '<small>', gettext('Added {offset_from_now} ago'), '</small>',
            '<small> - </small>',
            '<tpl if="delivery.last_feedback.is_passing_grade">',
                '<small class="success">', gettext('Passed'), '</small>',
            '<tpl else>',
                '<small class="danger">', gettext('Failed'), '</small>',
            '</tpl>',
            '<small> ({delivery.last_feedback.grade})</small>',
        '</div>'
    ],

    initComponent: function() {
        var col1TplCompiled = Ext.create('Ext.XTemplate', this.col1Tpl);
        Ext.apply(this, {
            cls: 'bootstrap',
            columns: [{
                header: 'data',
                dataIndex: 'id',
                flex: 1,
                sortable: false,
                menuDisabled: true,
                renderer: function(value, m, recentDeliveryRecord) {
                    var offset_from_now = recentDeliveryRecord.get('last_feedback').save_offset_from_now
                    return col1TplCompiled.apply({
                        delivery: recentDeliveryRecord.data,
                        offset_from_now: devilry_extjsextras.DatetimeHelpers.formatTimedeltaShort(offset_from_now)
                    });
                }
            }]
        });
        this.callParent(arguments);
    }
});
