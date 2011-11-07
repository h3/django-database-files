django-database-files
=====================

django-database-files is a storage system for Django that stores uploaded files 
in the database.

WARNING: It is generally a bad idea to serve static files from Django, 
but there are some valid use cases. If your Django app is behind a caching 
reverse proxy and you need to scale your application servers, it may be 
simpler to store files in the database.

Requires:

  * Django 1.1

Installation
------------

    $ python setup.py install

Usage
-----

In ``settings.py``, add ``database_files`` to your ``INSTALLED_APPS`` and add this line:

    DEFAULT_FILE_STORAGE = 'database_files.storage.DatabaseStorage'

In ``urls.py`` you must serve static files like this:

    if settings.DEV:
        if 'database_files' in settings.INSTALLED_APPS:
            urlpatterns += patterns('', 
                    url(r'^%s(.*)$' % settings.MEDIA_URL[1:], 'database_files.views.serve', 
                        {'document_root': 'media'}, name='database_file'),)
        else:
            urlpatterns += patterns('', (r'^%s(.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': 'media'}),)


All your ``FileField`` and ``ImageField`` files will now be stored in the 
database.

Test suite
----------

    $ ./run_tests.sh

