#!/usr/bin/env python
# Create the simplified database (replaces current db) and dump it to the fixture used in tests.

if __name__ == '__main__':
    from os.path import join
    from common import require_djangoproject, depends, getreporoot, dumpfixture

    require_djangoproject()
    depends('simplifiedtestdb')
    fixturepath = join(getreporoot(), 'devilry', 'simplified', 'fixtures',
                       'simplified', 'data.json')
    dumpfixture(fixturepath, 'core', 'auth.user')
