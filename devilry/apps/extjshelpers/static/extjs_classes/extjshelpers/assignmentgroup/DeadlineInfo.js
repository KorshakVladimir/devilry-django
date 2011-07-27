/** Deadline info.
 *
 * Lists deliveries within a Deadline using {@link
 * devilry.extjshelpers.assignmentgroup.DeliveryGrid}.
 */
Ext.define('devilry.extjshelpers.assignmentgroup.DeadlineInfo', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.deadlineinfo',
    cls: 'widget-deadlineinfo',
    margin: 10,
    requires: [
        'devilry.extjshelpers.assignmentgroup.DeliveryGrid'
    ],
    titleTpl: Ext.create('Ext.XTemplate', '{deadline:date}'),

    config: {
        /**
         * @cfg
         * The deadline data. The data attribute of a record returned from
         * loading the deadline from a store or model.
         */
        deadline: undefined,

        /**
         * @cfg
         * Delivery ``Ext.data.Model``.
         */
        deliverymodel: undefined
    },
    
    initComponent: function() {
        //var deliverystore = Ext.create('Ext.data.Store', {
            //model: this.deliverymodel,
            //remoteFilter: true,
            //remoteSort: true,
            //autoSync: true,
        //});

        deliverystore.proxy.extraParams.orderby = Ext.JSON.encode(['-number']);
        deliverystore.proxy.extraParams.filters = Ext.JSON.encode([{
            field: 'deadline',
            comp: 'exact',
            value: this.deadline.id
        }]);

        Ext.apply(this, {
            title: this.titleTpl.apply(this.deadline),
            items: [{
                xtype: 'deliverygrid',
                store: deliverystore
            }]
        });
        this.callParent(arguments);

        var me = this;
        deliverystore.addListener('load', function(store, records, successful) {
            if(successful) {
                if(records.length == 0) {
                    me.addDocked([{
                        dock: 'bottom',
                        xtype: 'toolbar',
                        items: [
                            'No deliveries on this deadline'
                        ]
                    }]);
                }
            }
        });
        deliverystore.load();
    }
});
