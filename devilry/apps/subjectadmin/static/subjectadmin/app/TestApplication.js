Ext.define('subjectadmin.TestApplication', {
    extend: 'subjectadmin.Application',

    controllers: [
        'ShortcutsTestMock',
        'Dashboard',
        'CreateNewAssignmentTestMock',
        'ChoosePeriodTestMock',
        'AssignmentTestMock'
    ],

    setupExtraRoutes: function() {
        // These views are only for unit tests
        this.route.add("/@@dashboard/shortcutlist", 'shortcutlist');
        this.route.add("/@@dashboard/actionlist", 'actionlist');
    },


    /*********************************************
     * Only for testing.
     ********************************************/
    shortcutlist: function() {
        this.setPrimaryContent({xtype: 'shortcutlist'});
    },

    actionlist: function() {
        this.setPrimaryContent({
            xtype: 'actionlist',
            data: {
                title: 'Action list test',
                links: [{
                    url: '#/@@actionitem-1',
                    text: 'Action item 1'
                }, {
                    url: '#/@@actionitem-2',
                    text: 'Action item 2'
                }]
            }
        });
    }
});
