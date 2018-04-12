# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup

setup(name='pytest-fxa',
      use_scm_version=True,
      description='pytest plugin for Firefox Accounts',
      long_description=open('README.rst').read(),
      author='Dave Hunt',
      author_email='dhunt@mozilla.com',
      url='https://github.com/davehunt/pytest-fxa',
      packages=['pytest_fxa'],
      install_requires=['PyFxA'],
      setup_requires=['setuptools_scm'],
      entry_points={'pytest11': ['fxa = pytest_fxa.plugin']},
      license='Mozilla Public License 2.0 (MPL 2.0)',
      keywords='py.test pytest mozilla automation firefox account fxa',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Framework :: Pytest',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: MacOS :: MacOS X',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing',
          'Topic :: Utilities',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy'])
