Ext.define( 'devilry_nodeadmin.model.Subject', {
    extend: 'Ext.data.Model',
    fields: [
        { name: 'id', type: 'int' },
        { name: 'short_name', type: 'string' },
        { name: 'long_name', type: 'string' }
    ]
});
