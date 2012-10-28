Ext.define('devilry_subjectadmin.view.passedpreviousperiod.SelectGroupsGrid', {
    extend: 'devilry_subjectadmin.view.passedpreviousperiod.GridBase',
    alias: 'widget.selectpassedpreviousgroupsgrid',
    cls: 'devilry_subjectadmin_selectpassedpreviousgroupssgrid bootstrap',
    requires: [
        'devilry_extjsextras.GridBigButtonCheckboxModel'
    ],

    initComponent: function() {
        Ext.apply(this, {
            selModel: Ext.create('devilry_extjsextras.GridBigButtonCheckboxModel'),
            tbar: [{
                text: gettext('Select'),
                menu: [{
                    text: gettext('Select all'),
                    listeners: {
                        scope: this,
                        click: this._onSelectAll
                    }
                }, {
                    text: gettext('Deselect all'),
                    listeners: {
                        scope: this,
                        click: this._onDeSelectAll
                    }
                }, '-', {
                    text: interpolate(gettext('Autodetected as previously passed'), {
                        period_term: gettext('period')
                    }, true),
                    listeners: {
                        scope: this,
                        click: this._onSelectPassingGradeInPreviousPeriod
                    }
                }]
            }]
        });
        this.callParent(arguments);
    },

    _onSelectAll: function() {
        this.getSelectionModel().selectAll();
    },
    _onDeSelectAll: function() {
        this.getSelectionModel().deselectAll();
    },

    _onSelectPassingGradeInPreviousPeriod: function() {
        this.selectWithPassingGradeInPrevious();
    },

    selectWithPassingGradeInPrevious: function() {
        var records = [];
        this.getStore().each(function(record) {
            if(record.get('oldgroup') !== null) {
                records.push(record);
            }
        });
        this.getSelectionModel().select(records);
    }
});
