# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import collections
import logging
import os
import random
import string

import pytest
from fxa.constants import ENVIRONMENT_URLS
from fxa.core import Client
from fxa.tests.utils import TestEmailAccount

here = os.path.dirname(__file__)
logging.getLogger(__name__).addHandler(logging.NullHandler())


def pytest_addoption(parser):
    group = parser.getgroup('fxa')
    group.addoption(
        '--fxa-email',
        action='store',
        dest='fxa_email',
        help='Email used to create fxa account.'
    )


@pytest.fixture(scope='session')
def fxa_client(fxa_urls):
    return Client(fxa_urls['authentication'])


@pytest.fixture(scope='session')
def fxa_urls(pytestconfig):
    return ENVIRONMENT_URLS[os.getenv('FXA_ENV', 'stage')]


@pytest.fixture
def fxa_email(pytestconfig):
    email = pytestconfig.getoption('fxa_email') or os.getenv('FXA_EMAIL')
    if email is None:
        return 'pytest-{:0x}@restmail.net'.format(random.getrandbits(10 * 4))
    return email


@pytest.fixture
def fxa_account(fxa_client, fxa_email):
    logger = logging.getLogger()
    account = TestEmailAccount(email=fxa_email)
    password = ''.join([random.choice(string.ascii_letters) for i in range(8)])
    FxAccount = collections.namedtuple('FxAccount', 'email password')
    fxa_account = FxAccount(email=account.email, password=password)
    session = fxa_client.create_account(fxa_account.email,
                                        fxa_account.password)
    logger.info('Created: {}'.format(fxa_account))
    account.fetch()
    message = account.wait_for_email(lambda m: 'x-verify-code' in m['headers'])
    session.verify_email_code(message['headers']['x-verify-code'])
    logger.info('Verified: {}'.format(fxa_account))
    yield fxa_account
    account.clear()
    fxa_client.destroy_account(fxa_account.email, fxa_account.password)
    logger.info('Removed: {}'.format(fxa_account))
