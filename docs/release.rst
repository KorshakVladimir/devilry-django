====================================
How to release a new Devilry version
====================================

In the devilry-django repo
##########################

1. Make sure you build and commit any changed ExtJS apps (see
   :doc:`javascript`). You will want to test that the built JS is working
   correctly with::

      $ bin/django_noextjsdebug.py runserver

2. Update the version number in::
   
      src/devilry/setup.py src/devilry/devilry/version.py docs/conf.py

3. Commit the version changes.
4. Add a releasenotes document in ``docs/releasenotes-X.Y.Z.rst``, and commit
   the new file.
5. Tag the release::

    $ git tag vX.Y.Z

6. Push the changes::

    $ git push
    $ git push --tags


In the devilry-deploy repo
##########################

.. note::

    Make sure all new develop (mr.developer fs) dependencies in
    ``buildout-base.cfg`` or ``buildout.cfg`` in the devilry code repo has been
    added to ``buildout/buildout-base.cfg`` before releasing a new version.

1. Update the version number in ``docs/src/conf.py``
2. Update the revision id in ``${buildout:extends}`` and
   ``${download-devilryrepo}`` in ``buildout/buildout-base.cfg``. Must use TAG,
   not branch name.
3. Add migration guide to ``docs/src/``, and remember to add the guide to ``migrationguidelisting.rst``.
4. Tag the release and push just like you did for devilry-django above.


In the devilry-userdoc repo
###########################
.. note:: this is not needed for RC, Beta releases.

1. Update the version number in ``conf.py``
2. Tag the release and push just like you did for devilry-django above.


.. note:: We plan on making this more streamlined in the future --- see :devilryissue:`384`.
