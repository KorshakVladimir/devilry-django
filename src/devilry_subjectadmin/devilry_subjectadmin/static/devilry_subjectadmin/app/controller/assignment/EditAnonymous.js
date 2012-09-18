/**
 * Controller for editing the anonymous attribute of an assignment.
 */
Ext.define('devilry_subjectadmin.controller.assignment.EditAnonymous', {
    extend: 'Ext.app.Controller',
    mixins: {
        'handleProxyError': 'devilry_subjectadmin.utils.DjangoRestframeworkProxyErrorMixin'
    },

    views: [
        'assignment.EditAnonymousPanel',
        'assignment.EditAnonymousWidget'
    ],

    controllers: [
        'assignment.Overview'
    ],

    models: ['Assignment'],

    refs: [{
        ref: 'cardContainer',
        selector: 'editanonymous-widget'
    }, {
        ref: 'readOnlyView',
        selector: 'editanonymous-widget editablesidebarbox#readAnonymous'

    }, {
        ref: 'editAnonymous',
        selector: 'editanonymous-widget editanonymouspanel'
    }, {
        ref: 'anonymousField',
        selector: 'editanonymous-widget editanonymouspanel checkbox'
    }, {
        ref: 'formPanel',
        selector: 'editanonymous-widget editanonymouspanel form'
    }, {
        ref: 'alertMessageList',
        selector: 'editanonymous-widget editanonymouspanel alertmessagelist'
    }],

    init: function() {
        // This is called when the application is initialized, not when the window is opened
        this.application.addListener({
            scope: this,
            assignmentSuccessfullyLoaded: this._onLoadAssignment
        });
        this.control({
            'editanonymous-widget editablesidebarbox': {
                edit: this._onEdit
            },
            'editanonymous-widget editanonymouspanel form checkbox': {
                render: this._onRenderForm
            },
            'editanonymous-widget editanonymouspanel #okbutton': {
                click: this._onSave
            },
            'editanonymous-widget editanonymouspanel #cancelbutton': {
                click: this._onCancel
            }
        });
    },

    _onLoadAssignment: function(assignmentRecord) {
        this.assignmentRecord = assignmentRecord;
        this.getReadOnlyView().enable();
        this._updateAnonymousWidget();
    },


    //////////////////////////////////
    //
    // The current stored value view
    //
    //////////////////////////////////
    
    _showReadView: function() {
        this.getCardContainer().getLayout().setActiveItem('readAnonymous');
    },

    _updateAnonymousWidget: function() {
        var anonymous = this.assignmentRecord.get('anonymous');
        var title, body;

        if(anonymous) {
            title = gettext('Anonymous');
            body = gettext('Examiners and students can not see each other and they can not communicate.');
        } else {
            title = gettext('Not anonymous');
            body = gettext('Examiners and students can see each other and communicate.');
        }
        var anonymous = this.assignmentRecord.get('anonymous');
        this.getReadOnlyView().updateTitle(title);
        this.getReadOnlyView().updateText(body);
    },

    _onEdit: function() {
        this._showEditView();
    },


    //////////////////////////////////
    //
    // Edit anonymous
    //
    //////////////////////////////////
    _showEditView: function() {
        this.getCardContainer().getLayout().setActiveItem('editAnonymous');
        this.getAnonymousField().setValue(this.assignmentRecord.get('anonymous'));
        Ext.defer(function() {
            this.getFormPanel().down('checkbox').focus();
        }, 100, this);
    },

    _onRenderForm: function() {
        this.getEditAnonymous().mon(this.getAssignmentModel().proxy, {
            scope: this,
            exception: this._onProxyError
        });
        this.getFormPanel().keyNav = Ext.create('Ext.util.KeyNav', this.getFormPanel().el, {
            enter: this._onSave,
            scope: this
        });
    },

    _onCancel: function() {
        this._showReadView();
    },

    _onSave: function() {
        this.getAlertMessageList().removeAll();
        var form = this.getFormPanel().getForm();
        var assignmentRecord = this.assignmentRecord;
        form.updateRecord(assignmentRecord);
        this._getMaskElement().mask(gettext('Saving ...'));
        assignmentRecord.save({
            scope: this,
            success: this._onSaveSuccess
        });
    },

    _getMaskElement: function() {
        return this.getFormPanel().getEl();
    },

    _onSaveSuccess: function() {
        this._getMaskElement().unmask();
        this._showReadView();
        this._updateAnonymousWidget();
    },

    _onProxyError: function(proxy, response, operation) {
        this._getMaskElement().unmask();
        this.handleProxyError(this.getAlertMessageList(), this.getFormPanel(),
            response, operation);
    }
});
