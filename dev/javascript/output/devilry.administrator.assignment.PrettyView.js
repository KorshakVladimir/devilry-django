Ext.data.JsonP.devilry_administrator_assignment_PrettyView({
  "mixedInto": [

  ],
  "href": "PrettyView2.html#devilry-administrator-assignment-PrettyView",
  "allMixins": [

  ],
  "doc": "<p>PrettyView for an assignment.</p>\n",
  "singleton": false,
  "html_filename": "PrettyView2.html",
  "code_type": "ext_define",
  "subclasses": [

  ],
  "superclasses": [
    "devilry.administrator.PrettyView"
  ],
  "protected": false,
  "tagname": "class",
  "mixins": [

  ],
  "members": {
    "cfg": [
      {
        "type": "Object",
        "href": "PrettyView.html#devilry-administrator-PrettyView-cfg-",
        "owner": "devilry.administrator.PrettyView",
        "doc": "<p>Optional list of menuitems for plugin actions.</p>\n",
        "html_filename": "PrettyView.html",
        "protected": false,
        "tagname": "cfg",
        "static": false,
        "private": false,
        "inheritable": false,
        "alias": null,
        "name": "",
        "linenr": 46,
        "filename": "/Volumes/viktig/code/devilry-django/devilry/apps/administrator/static/extjs_classes/administrator/PrettyView.js",
        "deprecated": null
      },
      {
        "type": "Object",
        "href": "PrettyView2.html#devilry-administrator-assignment-PrettyView-cfg-assignmentgroupmodelname",
        "owner": "devilry.administrator.assignment.PrettyView",
        "doc": "<p>The name of the assignment group <code>Ext.data.Model</code> to use in the store\n(Required).  The store copies the proxy from this model.</p>\n",
        "html_filename": "PrettyView2.html",
        "protected": false,
        "tagname": "cfg",
        "static": false,
        "private": false,
        "inheritable": false,
        "alias": null,
        "name": "assignmentgroupmodelname",
        "shortDoc": "The name of the assignment group Ext.data.Model to use in the store\n(Required). ...",
        "linenr": 17,
        "filename": "/Volumes/viktig/code/devilry-django/devilry/apps/administrator/static/extjs_classes/administrator/assignment/PrettyView.js",
        "deprecated": null
      },
      {
        "type": "Object",
        "href": "PrettyView.html#devilry-administrator-PrettyView-cfg-bodyTpl",
        "owner": "devilry.administrator.PrettyView",
        "doc": "<p>A <code>Ext.XTemplate</code> object for the body of this view. (Required).</p>\n",
        "html_filename": "PrettyView.html",
        "protected": false,
        "tagname": "cfg",
        "static": false,
        "private": false,
        "inheritable": false,
        "alias": null,
        "name": "bodyTpl",
        "shortDoc": "A Ext.XTemplate object for the body of this view. ...",
        "linenr": 27,
        "filename": "/Volumes/viktig/code/devilry-django/devilry/apps/administrator/static/extjs_classes/administrator/PrettyView.js",
        "deprecated": null
      },
      {
        "type": "Object",
        "href": "PrettyView.html#devilry-administrator-PrettyView-cfg-dashboardUrl",
        "owner": "devilry.administrator.PrettyView",
        "doc": "<p>The url to the dashboard. (Required). Used after delete to return to\nthe dashboard.</p>\n",
        "html_filename": "PrettyView.html",
        "protected": false,
        "tagname": "cfg",
        "static": false,
        "private": false,
        "inheritable": false,
        "alias": null,
        "name": "dashboardUrl",
        "shortDoc": "The url to the dashboard. ...",
        "linenr": 39,
        "filename": "/Volumes/viktig/code/devilry-django/devilry/apps/administrator/static/extjs_classes/administrator/PrettyView.js",
        "deprecated": null
      },
      {
        "type": "Object",
        "href": "PrettyView.html#devilry-administrator-PrettyView-cfg-modelname",
        "owner": "devilry.administrator.PrettyView",
        "doc": "<p>The name of the <code>Ext.data.Model</code> to present in the body. (Required).</p>\n",
        "html_filename": "PrettyView.html",
        "protected": false,
        "tagname": "cfg",
        "static": false,
        "private": false,
        "inheritable": false,
        "alias": null,
        "name": "modelname",
        "shortDoc": "The name of the Ext.data.Model to present in the body. ...",
        "linenr": 15,
        "filename": "/Volumes/viktig/code/devilry-django/devilry/apps/administrator/static/extjs_classes/administrator/PrettyView.js",
        "deprecated": null
      },
      {
        "type": "Object",
        "href": "PrettyView.html#devilry-administrator-PrettyView-cfg-objectid",
        "owner": "devilry.administrator.PrettyView",
        "doc": "<p>Unique ID of the object to load from the model. (Required).</p>\n",
        "html_filename": "PrettyView.html",
        "protected": false,
        "tagname": "cfg",
        "static": false,
        "private": false,
        "inheritable": false,
        "alias": null,
        "name": "objectid",
        "shortDoc": "Unique ID of the object to load from the model. ...",
        "linenr": 21,
        "filename": "/Volumes/viktig/code/devilry-django/devilry/apps/administrator/static/extjs_classes/administrator/PrettyView.js",
        "deprecated": null
      },
      {
        "type": "Object",
        "href": "PrettyView.html#devilry-administrator-PrettyView-cfg-relatedButtons",
        "owner": "devilry.administrator.PrettyView",
        "doc": "<p>Optional list of buttons for related actions.</p>\n",
        "html_filename": "PrettyView.html",
        "protected": false,
        "tagname": "cfg",
        "static": false,
        "private": false,
        "inheritable": false,
        "alias": null,
        "name": "relatedButtons",
        "linenr": 33,
        "filename": "/Volumes/viktig/code/devilry-django/devilry/apps/administrator/static/extjs_classes/administrator/PrettyView.js",
        "deprecated": null
      }
    ],
    "event": [
      {
        "href": "PrettyView.html#devilry-administrator-PrettyView-event-edit",
        "owner": "devilry.administrator.PrettyView",
        "params": [
          {
            "type": "Ext.model.Model",
            "doc": "<p>The record to edit.</p>\n",
            "optional": false,
            "name": "record"
          },
          {
            "type": "Object",
            "doc": "<p>The edit button.</p>\n",
            "optional": false,
            "name": "button"
          },
          {
            "type": "Object",
            "doc": "<p>The options object passed to Ext.util.Observable.addListener.</p>\n",
            "tagname": "param",
            "name": "options"
          }
        ],
        "doc": "<p>Fired when the edit button is clicked.</p>\n",
        "html_filename": "PrettyView.html",
        "protected": false,
        "tagname": "event",
        "static": false,
        "private": false,
        "inheritable": false,
        "alias": null,
        "name": "edit",
        "shortDoc": "Fired when the edit button is clicked. ...",
        "linenr": 62,
        "filename": "/Volumes/viktig/code/devilry-django/devilry/apps/administrator/static/extjs_classes/administrator/PrettyView.js",
        "deprecated": null
      },
      {
        "href": "PrettyView.html#devilry-administrator-PrettyView-event-loadmodel",
        "owner": "devilry.administrator.PrettyView",
        "params": [
          {
            "type": "Ext.model.Model",
            "doc": "<p>The loaded record.</p>\n",
            "optional": false,
            "name": "record"
          },
          {
            "type": "Object",
            "doc": "<p>The options object passed to Ext.util.Observable.addListener.</p>\n",
            "tagname": "param",
            "name": "options"
          }
        ],
        "doc": "<p>Fired when the model record is loaded successfully.</p>\n",
        "html_filename": "PrettyView.html",
        "protected": false,
        "tagname": "event",
        "static": false,
        "private": false,
        "inheritable": false,
        "alias": null,
        "name": "loadmodel",
        "shortDoc": "Fired when the model record is loaded successfully. ...",
        "linenr": 55,
        "filename": "/Volumes/viktig/code/devilry-django/devilry/apps/administrator/static/extjs_classes/administrator/PrettyView.js",
        "deprecated": null
      }
    ],
    "property": [

    ],
    "method": [
      {
        "href": "PrettyView.html#devilry-administrator-PrettyView-method-setRecord",
        "owner": "devilry.administrator.PrettyView",
        "params": [
          {
            "type": "Object",
            "doc": "\n",
            "optional": false,
            "name": "record"
          }
        ],
        "doc": "<p>Set record. Triggers the loadmodel event.</p>\n",
        "html_filename": "PrettyView.html",
        "protected": false,
        "tagname": "method",
        "static": false,
        "return": {
          "type": "void",
          "doc": "\n"
        },
        "private": false,
        "inheritable": false,
        "alias": null,
        "name": "setRecord",
        "shortDoc": "Set record. ...",
        "linenr": 170,
        "filename": "/Volumes/viktig/code/devilry-django/devilry/apps/administrator/static/extjs_classes/administrator/PrettyView.js",
        "deprecated": null
      }
    ],
    "css_var": [

    ],
    "css_mixin": [

    ]
  },
  "static": false,
  "author": null,
  "private": false,
  "inheritable": false,
  "alias": null,
  "alternateClassNames": [

  ],
  "statics": {
    "cfg": [

    ],
    "event": [

    ],
    "property": [

    ],
    "method": [

    ],
    "css_var": [

    ],
    "css_mixin": [

    ]
  },
  "name": "devilry.administrator.assignment.PrettyView",
  "linenr": 1,
  "xtypes": [
    "administrator_assignmentprettyview"
  ],
  "component": false,
  "filename": "/Volumes/viktig/code/devilry-django/devilry/apps/administrator/static/extjs_classes/administrator/assignment/PrettyView.js",
  "deprecated": null,
  "extends": "devilry.administrator.PrettyView",
  "docauthor": null
});