ACP-Calendar
=============================

.. image:: https://badge.fury.io/py/acp-calendar.png
    :target: https://badge.fury.io/py/acp-calendar


.. image:: https://api.travis-ci.org/luiscberrocal/django-acp-calendar.svg?branch=master
    :target: https://travis-ci.org/luiscberrocal/acp-calendar


.. image:: https://coveralls.io/repos/github/luiscberrocal/django-acp-calendar/badge.svg?branch=master
    :target: https://coveralls.io/github/luiscberrocal/django-acp-calendar?branch=master

.. image:: https://codeclimate.com/github/luiscberrocal/django-acp-calendar/badges/gpa.svg
   :target: https://codeclimate.com/github/luiscberrocal/django-acp-calendar
   :alt: Code Climate


Holiday calendar and date management for the Panama Canal. Includes Panama Canal holidays from 2006 to 2017.

Documentation
-------------

The full documentation is at https://acp-calendar.readthedocs.org.

Quickstart
----------

Install ACP-Calendar::

    pip install acp-calendar


Open your settings file and include acp_calendar and rest_framework to the THIRD_PARTY_APPS variable on your settings
file.

The settings file::

    DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
    )
    THIRD_PARTY_APPS = (
        'crispy_forms',  # Form layouts
        'allauth',  # registration
        'allauth.account',  # registration
        'allauth.socialaccount',  # registration
        'rest_framework',
        'acp_calendar',
    )

    # Apps specific for this project go here.
    LOCAL_APPS = (
        'acp_calendar_project.users',  # custom users app

        # Your stuff: custom apps go here
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


Add the acp_calendar.urls to your urls file.::

    urlpatterns = [
        url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
        url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),

        # Django Admin, use {% url 'admin:index' %}
        url(settings.ADMIN_URL, include(admin.site.urls)),

        # User management
        url(r'^users/', include('acp_calendar_project.users.urls', namespace='users')),
        url(r'^calendar/', include('acp_calendar.urls', namespace='calendar')),
        url(r'^accounts/', include('allauth.urls')),

        # Your stuff: custom urls includes go here


    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





Features
--------

To get the working days for the Panama Canal between january 1st to january 31st 2016.

::

     import acp_calendar

     start_date = datetime.date(2016, 1,1)
     end_date = datetime.date(2016,1,31)
     working_days = ACPHoliday.get_working_days(start_date, end_date)


To access the calculator go to http://<your_host>:<your_port>/calendar/calculator/

To use the calculator your base.html must have:

    * A javascript block at the end of the html
    * jQuery (version 2.2.x)
    * jQuery ui (version 1.12.x)



Virtual Environment
--------------------

Use virtualenv to manage a virtual environment.

In a Mac use the following command to create the virtual environment::

    python3 /usr/local/lib/python3.4/site-packages/virtualenv.py --no-site-packages acp_calendar_env


Running Tests
--------------

Does the code actually work?

::

    source acp_calendar_env/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python runtests.py

Builds
---------

We are using Travis for continuos integration https://travis-ci.org/luiscberrocal/django-acp-calendar/builds

For coverage we are using coveralls https://coveralls.io/github/luiscberrocal/django-acp-calendar

Run bumpversion ::

    $ bumpversion minor


Instead of minor you could also use major o patch depending on the level of the release.

::

    python setup.py sdist bdist_wheel

    python setup.py register -r pypitest

    python setup.py sdist upload -r pypitest



Check https://testpypi.python.org/pypi/acp-calendar/

 ::

    python setup.py register -r pypi

    python setup.py sdist upload -r pypi


Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
