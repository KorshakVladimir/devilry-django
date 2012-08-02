{% extends "administrator/base.django.js" %}
{% load extjs %}


{% block imports %}
    {{ block.super }}
    Ext.require('devilry.administrator.Dashboard');
{% endblock %}


{% block onready %}
    Ext.create('Ext.container.Viewport', {
        layout: 'border',
        style: 'background-color: transparent',
        items: [{
            region: 'north',
            xtype: 'devilryheader',
            navclass: 'administrator'
        }, {
            region: 'south',
            xtype: 'pagefooter'
        }, {
            region: 'center',
            xtype: 'administrator-dashboard',
            border: false,
            padding: '0 20 0 20',
            dashboardUrl: DASHBOARD_URL
        }]
    });
{% endblock %}
