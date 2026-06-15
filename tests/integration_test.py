"""Behavioral tests for the tox-towncrier plugin."""

from __future__ import annotations

import typing as _t

import pytest


if _t.TYPE_CHECKING:
    from pytest_subtests import SubTests

    from tox.pytest import ToxProjectCreator


def test_changelog_envs_registered(
    tox_project: ToxProjectCreator,
    subtests: SubTests,
) -> None:
    """The plugin contributes ``make-``/``check-``/``draft-changelog`` envs.

    :param tox_project: Tox-provided project factory fixture.
    :param subtests: Pytest's subtest fixture for granular reporting.
    """
    project = tox_project({'tox.ini': '[tox]\n'})
    tox_invocation_result = project.run('list')
    tox_invocation_result.assert_success()
    for env_name in ('make-changelog', 'check-changelog', 'draft-changelog'):
        with subtests.test(msg=env_name):
            assert env_name in tox_invocation_result.out


@pytest.mark.parametrize(
    ('env_name', 'extra_args', 'expected_present', 'expected_absent'),
    (
        pytest.param(
            'make-changelog',
            (),
            ('towncrier.build', '[UNRELEASED DRAFT]', '--draft'),
            (),
            id='make-changelog-default-unreleased-draft',
        ),
        pytest.param(
            'make-changelog',
            ('--', '1.3.2'),
            ('towncrier.build', '1.3.2'),
            ('[UNRELEASED DRAFT]',),
            id='make-changelog-with-version',
        ),
        pytest.param(
            'check-changelog',
            (),
            ('towncrier.check', 'origin/devel'),
            (),
            id='check-changelog-default',
        ),
        pytest.param(
            'draft-changelog',
            (),
            ('sh -c', 'towncrier.build'),
            (),
            id='draft-changelog-default',
        ),
    ),
)
def test_env_commands(  # pylint: disable=too-many-arguments
    *,
    tox_project: ToxProjectCreator,
    env_name: str,
    extra_args: tuple[str, ...],
    expected_present: tuple[str, ...],
    expected_absent: tuple[str, ...],
    subtests: SubTests,
) -> None:
    """The plugin's envs produce the expected ``commands`` config.

    :param tox_project: Tox-provided project factory fixture.
    :param env_name: Name of the env to query.
    :param extra_args: Extra CLI arguments to append to the ``tox`` call,
        including the ``--`` separator and any positional arguments.
    :param expected_present: Substrings that must appear in the output.
    :param expected_absent: Substrings that must not appear in the output.
    :param subtests: Pytest's subtest fixture for granular reporting.
    """
    project = tox_project({'tox.ini': '[tox]\n'})
    tox_invocation_result = project.run(
        'config',
        '-e',
        env_name,
        '-k',
        'commands',
        *extra_args,
    )
    tox_invocation_result.assert_success()
    for substring in expected_present:
        with subtests.test(msg=f'present:{substring}'):
            assert substring in tox_invocation_result.out
    for substring in expected_absent:
        with subtests.test(msg=f'absent:{substring}'):
            assert substring not in tox_invocation_result.out
