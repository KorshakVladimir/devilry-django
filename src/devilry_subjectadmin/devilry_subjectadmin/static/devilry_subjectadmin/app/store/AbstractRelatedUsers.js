Ext.define('devilry_subjectadmin.store.AbstractRelatedUsers', {
    extend: 'Ext.data.Store',

    requires: [
        'devilry_extjsextras.DjangoRestframeworkProxyErrorHandler',
        'devilry_extjsextras.HtmlErrorDialog'
    ],

    loadInPeriod: function(periodId, loadConfig) {
        this.setPeriod(periodId);
        this.load(loadConfig);
    },

    setPeriod: function(periodId) {
        this.proxy.url = Ext.String.format(this.proxy.urlpatt, periodId);
    },


    /**
     * @param {Function} [config.success]
     *     Callback invoked in ``config.scope``
     *     when the store loads successfully. Parameters are ``records`` and
     *     ``operation``.
     * @param {Boolean} [config.scope]
     *     Scope to invoke ``config.success`` in.
     * @param {String} [config.errortitle] The title of the error message shown on load error.
     */
    loadWithAutomaticErrorHandling: function(config) {
        this.load({
            scope: this,
            callback: function(records, operation) {
                if(operation.success) {
                    Ext.callback(config.success, config.scope, [records, operation]);
                } else {
                    this._onLoadFailure(operation, config.errortitle);
                }
            }
        });
    },
    _onLoadFailure: function(operation, errortitle) {
        var error = Ext.create('devilry_extjsextras.DjangoRestframeworkProxyErrorHandler', operation);
        error.addErrors(null, operation);
        var errormessage = error.asHtmlList();
        Ext.widget('htmlerrordialog', {
            title: errortitle,
            bodyHtml: errormessage
        }).show();
    }
});
