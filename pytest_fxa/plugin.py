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
from fxa.errors import ClientError
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


def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'fxa_env(name,): mark tests to run against named Firefox Accounts '
        'environment(s): ' + ', '.join(ENVIRONMENT_URLS.keys()))


def pytest_generate_tests(metafunc):
    if 'fxa_urls' not in metafunc.fixturenames:
        return

    envs = set([
        env_name
        for marker in metafunc.definition.iter_markers('fxa_env')
        for env_name in marker.args])

    if envs:
        metafunc.parametrize('fxa_urls', envs, indirect=True)


@pytest.fixture
def fxa_client(fxa_urls):
    return Client(fxa_urls['authentication'])


@pytest.fixture
def fxa_urls(request):
    env = getattr(request, 'param', os.getenv('FXA_ENV', 'stage'))
    return ENVIRONMENT_URLS[env]


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
    try:
        account.clear()
        fxa_client.destroy_account(fxa_account.email, fxa_account.password)
        logger.info('Removed: {}'.format(fxa_account))
    except ClientError as e:
        # 'Unknown Account' error is ok - account already deleted
        # https://github.com/mozilla/fxa-auth-server/blob/master/docs/api.md#response-format
        if e.errno not in [102]:
            raise
