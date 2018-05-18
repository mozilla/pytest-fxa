pytest-fxa
==========

pytest-fxa is a plugin for pytest_ that provides test accounts for
`Firefox Accounts`_.

.. image:: https://img.shields.io/badge/license-MPL%202.0-blue.svg
   :target: https://github.com/mozilla/pytest-fxa/blob/master/LICENSE
   :alt: License
.. image:: https://img.shields.io/pypi/v/pytest-fxa.svg
   :target: https://pypi.python.org/pypi/pytest-fxa/
   :alt: PyPI
.. image:: https://img.shields.io/travis/mozilla/pytest-fxa.svg
   :target: https://travis-ci.org/mozilla/pytest-fxa/
   :alt: Travis
.. image:: https://img.shields.io/github/issues-raw/mozilla/pytest-fxa.svg
   :target: https://github.com/mozilla/pytest-fxa/issues
   :alt: Issues
.. image:: https://pyup.io/repos/github/mozilla/pytest-fxa/shield.svg
  :target: https://pyup.io/repos/github/mozilla/pytest-fxa
  :alt: Updates
.. image:: https://pyup.io/repos/github/mozilla/pytest-fxa/python-3-shield.svg
  :target: https://pyup.io/repos/github/mozilla/pytest-fxa/
  :alt: Python 3

Requirements
------------

You will need the following prerequisites in order to use pytest-fxa:

- Python 2.7, 3.6, PyPy, or PyPy3

Installation
------------

To install pytest-fxa:

.. code-block:: bash

  $ pip install pytest-fxa

Creating a test Firefox Account
-------------------------------

To create a Firefox Account for testing, include the ``fxa_account`` fixture
name in your test method signature. This is a tuple with named properties for
the test account's ``email`` and ``password``. The following example shows how
this could be used with `Selenium`_ to sign into a website that uses Firefox
Accounts for authentication:

.. code-block:: python

  def test_my_fxa_site(fxa_account, selenium):
      selenium.get('https://example.com/')
      selenium.find_element(By.ID, 'email').send_keys(fxa_account.email)
      selenium.find_element(By.ID, 'password').send_keys(fxa_account.password)
      selenium.find_element(By.ID, 'login').click()

The test account will be automatically destroyed when it's no longer needed.

Specifying an environment
-------------------------

By default all accounts will be created on the 'stage' environment. You can set
the ``FXA_ENV`` environment variable to target 'production' or 'stable'.
Alternatively, you can override the ``fxa_urls`` fixture to specify the URL for
you environment:

.. code-block:: python

  @pytest.fixture
  def fxa_urls():
      return {
          'authentication': 'https://api-accounts.stage.mozaws.net/v1',
          'oauth': 'https://oauth.stage.mozaws.net/v1',
          'content': 'https://accounts.stage.mozaws.net/',
          'profile': 'https://profile.stage.mozaws.net/v1',
          'token': 'https://token.stage.mozaws.net/'}

Resources
---------

- `Release Notes`_
- `Issue Tracker`_
- Code_

.. _pytest: http://www.python.org/
.. _Firefox Accounts: https://developer.mozilla.org/en-US/docs/Mozilla/Tech/Firefox_Accounts
.. _Selenium: https://www.seleniumhq.org/
.. _Release Notes:  http://github.com/mozilla/pytest-fxa/blob/master/CHANGES.rst
.. _Issue Tracker: http://github.com/mozilla/pytest-fxa/issues
.. _Code: http://github.com/mozilla/pytest-fxa
