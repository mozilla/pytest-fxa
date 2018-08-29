# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random
import string

import pytest
from fxa.core import Session

from pytest_fxa import plugin


@pytest.fixture
def random_email():
    test_string = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(8)
    )
    return "{}@restmail.net".format(test_string)


def test_login(testdir):
    testdir.makepyfile(
        """
        from fxa.core import Client

        def test_login(fxa_account, fxa_client):
            assert fxa_client.login(fxa_account.email, fxa_account.password)
    """
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_no_digits_in_password(testdir):
    testdir.makepyfile(
        """
        import re

        def test_login(fxa_account):
            assert re.search(r'\d', fxa_account.password) is None
    """
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_destroyed(testdir):
    testdir.makepyfile(
        """
        def test_destroy(fxa_client, fxa_account):
            for _ in range(2):
                fxa_client.destroy_account(
                    fxa_account.email, fxa_account.password)
    """
    )
    result = testdir.runpytest()
    result.assert_outcomes(failed=1)
    assert "ClientError: Unknown account" in result.stdout.str()


def test_cleanup_when_destroyed(testdir):
    testdir.makepyfile(
        """
        def test_destroy(fxa_client, fxa_account):
            fxa_client.destroy_account(fxa_account.email, fxa_account.password)
    """
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_commandline_email_option(testdir, random_email):
    testdir.makepyfile(
        """
        import pytest

        def test_account(fxa_account):
            assert '{}' == fxa_account.email
    """.format(
            random_email
        )
    )
    result = testdir.runpytest("--fxa-email", random_email)
    result.assert_outcomes(passed=1)


def test_fxa_email_env_variable(testdir, monkeypatch, random_email):
    monkeypatch.setenv("FXA_EMAIL", "{}".format(random_email))
    testdir.makepyfile(
        """
        import pytest

        def test_account(fxa_account):
            assert '{}' == fxa_account.email
    """.format(
            random_email
        )
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_no_email_given(testdir):
    testdir.makepyfile(
        """
        import pytest

        def test_account(fxa_account):
            assert 'pytest-' in fxa_account.email
    """
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_fxa_env_env_variable(monkeypatch, testdir):
    env = "stable"
    monkeypatch.setenv("FXA_ENV", env)
    testdir.makepyfile(
        """
        import pytest

        def test_account(fxa_urls):
            assert '{0}' in fxa_urls['authentication']
    """.format(
            env
        )
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_fxa_env_marker(monkeypatch, testdir):
    env, marker = ["stable", "stage"]
    monkeypatch.setenv("FXA_ENV", env)
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.fxa_env('{0}')
        def test_account(fxa_urls):
            assert '{0}' in fxa_urls['authentication']
    """.format(
            marker
        )
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_fxa_env_marker_multi(monkeypatch, testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.fxa_env('stable', 'stage')
        def test_account(fxa_urls): pass
    """
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=2)


def test_fxa_env_marker_empty(monkeypatch, testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.fxa_env()
        def test_account(fxa_urls):
            assert 'stage' in fxa_urls['authentication']
    """
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_cleanup_after_failed_verification(mocker, testdir):
    mock = mocker.Mock(side_effect=Exception)
    mocker.patch.object(Session, "verify_email_code", mock)
    mocker.spy(plugin, "fxa_cleanup")

    testdir.makepyfile(
        """
        import pytest

        def test_login(fxa_account, fxa_client):
            assert fxa_client.login(fxa_account.email, fxa_account.password)
    """
    )
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert plugin.fxa_cleanup.call_count == 1
