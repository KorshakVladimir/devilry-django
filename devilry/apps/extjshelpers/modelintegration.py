import json
from fieldintegration import field_to_extjstype


def _recurse_get_fkfield(modelcls, path):
    cur = modelcls._meta.get_field(path.pop(0))
    if not path:
        return cur
    else:
        return _recurse_get_fkfield(cur.related.model, path)


def _iter_fields(simplifiedcls):
    meta = simplifiedcls._meta
    for fieldname in meta.resultfields.always_available_fields:
        if "__" in fieldname:
            path = fieldname.split('__')
            yield fieldname, _recurse_get_fkfield(meta.model, path)
        else:
            yield fieldname, meta.model._meta.get_field(fieldname)



def get_extjs_modelname(restfulmodelcls):
    simplified = restfulmodelcls._meta.simplified
    return '{module}.{name}'.format(module=simplified.__module__, name=simplified.__name__)


def restfulmodelcls_to_extjsmodel(restfulmodelcls):
    modelfields = []
    for fieldname, field in _iter_fields(restfulmodelcls._meta.simplified):
        exttype = field_to_extjstype(field, fieldname)
        modelfields.append(dict(name=fieldname, type=exttype))
    for fieldname in restfulmodelcls._meta.urlmap:
        modelfields.append(dict(name=fieldname, type='string'))
    return """Ext.define('{modelname}', {{
            extend: 'Ext.data.Model',
            fields: {modelfields},
            idProperty: '{idprop}',
            proxy: {{
                type: 'rest',
                url: '{resturl}',
                extraParams: {{getdata_in_qrystring: true}},
                reader: {{
                    type: 'json',
                    root: 'items'
                }},
                writer: {{
                    type: 'json'
                }}
            }}
        }});""".format(modelname = get_extjs_modelname(restfulmodelcls),
                      modelfields = json.dumps(modelfields),
                      idprop = 'id', # TODO: metaoption
                      resturl = restfulmodelcls.get_rest_url())
