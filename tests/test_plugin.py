# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def test_login(testdir):
    testdir.makepyfile("""
        from fxa.core import Client

        def test_login(fxa_account, fxa_client):
            assert fxa_client.login(fxa_account.email, fxa_account.password)
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_no_digits_in_password(testdir):
    testdir.makepyfile("""
        import re

        def test_login(fxa_account):
            assert re.search(r'\d', fxa_account.password) is None
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_destroyed(testdir):
    testdir.makepyfile("""
        def test_destroy(fxa_client, fxa_account):
            fxa_client.destroy_account(fxa_account.email, fxa_account.password)
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1, passed=1)
    assert 'ClientError: Unknown account' in result.stdout.str()
