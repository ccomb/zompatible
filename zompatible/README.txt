==================
Zompatible project
==================

Requirements:
 + python2.4
 + gcc >= 4.0

To start contributing to the project, you need to run some scripts to initialize
the development environment::

    python2.4 ./bootstrap.py 
    ./bin/buildout
    ./bin/buildout

Remark: The first run of ./bin/buildout generates an error because the bootstrap
script retreives the most recent version of buildout but zope3.4/versions.cfg
freezes the setuptools version to 0.6c7. Rerun buildout to go ahead and replace
setuptools with the older version.
TODO: fix setuptools version conflict.

You can now check that the tests can be running::

    ./bin/test


