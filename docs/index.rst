======================================================================
Devilry developer documentation overview
======================================================================


.. note::
    Welcome to the Devilry developer documentation.
    See http://devilry.org/ for general information about Devilry,
    and https://github.com/devilry/devilry-django for the code.


#######################################################################
Common topics (see Table of contents for all topics)
#######################################################################


Core
----------------------------------------------------------------------


.. module:: devilry.apps.core

* **devilry.apps.core.models:** :ref:`API <devilry.apps.core.models>`
* :ref:`userobj`
* :ref:`devilry.apps.core.deliverystore <devilry.apps.core.deliverystore>`


Essential information for new developers
----------------------------------------
* :ref:`devenv`
* :ref:`sourceorganized`
* :ref:`buildout`
* :ref:`testsuite`
* :ref:`testhelper`
* :ref:`javascript`
* More info available on the `Developer wiki page <https://github.com/devilry/devilry-django/wiki/Developer>`_.


How to document Devilry
---------------------------------------------------------------------
* `How to write API documentation - wiki page <https://github.com/devilry/devilry-django/wiki/How-to-write-API-documentation>`_
* :ref:`readthedocs` --- If you need to debug build errors from readthedocs.org.


Extending Devilry
----------------------------------------------------------------------

* :doc:`extend_devilry`
* **Plugins:** :ref:`plugins`, :ref:`Overview <apps.gradeeditors>`,
  :doc:`Qualifies for exam <devilry_qualifiesforexam>`.
* **Apps**: Read the `Django docs <https://www.djangoproject.com/>`_.


RESTful API
----------------------------------------------------------------------

* **Old rest APIs**: See the old docs: http://devilry.org/devilry-django/dev/.
  These are deprecated and will be remove soon.
* **New rest APIs**: We are missing a listing of the URLs of all our new APIs,
  so please contact us (see http://devilry.org) if you need help finding them.


Apps
----------------------------------------------------------------------

* :ref:`devilry_subjectadmin`
* :doc:`devilry_qualifiesforexam`
* :doc:`devilry_search`

.. note:: The apps listing is incomplete.


#######################################################################
Releases
#######################################################################

* :ref:`releasenoteslisting`


#######################################################################
Table of contents
#######################################################################
.. toctree::
    :maxdepth: 2

    core.models
    userobj
    core.deliverystore

    devenv
    sourceorganized
    buildout
    testsuite
    testhelper
    extend_devilry
    create_app
    plugins

    devilry_subjectadmin
    devilry_qualifiesforexam
    devilry_search

    apps.gradeeditors
    devilry.utils

    readthedocs
    i18n
    javascript
    pycharm

    releasenoteslisting
    release



#######################################################################
Indices and tables
#######################################################################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

