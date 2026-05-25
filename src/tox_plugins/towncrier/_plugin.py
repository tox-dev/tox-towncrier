"""A tox plugin providing Towncrier changelog environments."""

from __future__ import annotations

import typing as _t
from shlex import join as shlex_join

from tox.config.loader.memory import MemoryLoader
from tox.plugin import impl


if _t.TYPE_CHECKING:
    from collections import abc as _c  # noqa: WPS347

    from tox.config.sets import ConfigSet
    from tox.session.state import State


_PYTHON_CLI_OPTIONS = (
    'python',
    '-bb',
    '-E',
    '-s',
    '-I',
    '-Werror',
)


@impl
def tox_extend_envs() -> _c.Iterable[str]:
    """Declare the Towncrier changelog environments.

    :returns: The names of the tox environments this plugin provides.
    """
    return ('make-changelog', 'check-changelog', 'draft-changelog')


@impl
def tox_add_core_config(
    core_conf: ConfigSet,  # noqa: ARG001  # pylint: disable=unused-argument
    state: State,
) -> None:
    """Inject default configuration for Towncrier environments.

    :param core_conf: The core tox configuration set (unused).
    :param state: The tox session state to inject environments into.
    """
    pos_args = state.conf.pos_args(to_path=None)

    _inject_make_changelog(state, pos_args)
    _inject_check_changelog(state, pos_args)
    _inject_draft_changelog(state)


def _inject_make_changelog(
    state: State,
    pos_args: tuple[str, ...] | None,
) -> None:
    version_args: tuple[str, ...]
    if pos_args is None:
        # No posargs: produce an unreleased draft
        version_args = ('[UNRELEASED DRAFT]', '--draft')
    else:
        # User passed a version: tox -e make-changelog -- 1.3.2
        version_args = pos_args

    make_cmd = (
        *_PYTHON_CLI_OPTIONS,
        '-m',
        'towncrier.build',
        '--version',
        *version_args,
    )

    state.conf.memory_seed_loaders['make-changelog'].append(
        MemoryLoader(
            base=[],
            description=(
                '[tox-towncrier] Generate a changelog from fragments using '
                'Towncrier. Getting an unreleased changelog preview does not '
                'require extra arguments. When invoking to update the '
                'changelog, pass the desired version as an argument after '
                '`--`. For example, `tox -e make-changelog -- 1.3.2`.'
            ),
            deps=['towncrier'],
            depends=['check-changelog'],
            commands_pre=[],
            commands=[shlex_join(make_cmd)],
            commands_post=[],
            package='skip',
            skip_install='true',
        ),
    )


def _inject_check_changelog(
    state: State,
    pos_args: tuple[str, ...] | None,
) -> None:
    check_cmd = (
        *_PYTHON_CLI_OPTIONS,
        '-m',
        'towncrier.check',
        '--compare-with',
        'origin/devel',
        *(() if pos_args is None else pos_args),
    )

    state.conf.memory_seed_loaders['check-changelog'].append(
        MemoryLoader(
            base=[],
            description='[tox-towncrier] Check Towncrier change notes',
            deps=['towncrier'],
            commands_pre=[],
            commands=[shlex_join(check_cmd)],
            commands_post=[],
            package='skip',
            skip_install='true',
        ),
    )


def _inject_draft_changelog(state: State) -> None:
    draft_inner_cmd = (
        *_PYTHON_CLI_OPTIONS,
        '-m',
        'towncrier.build',
        '--version',
        '[UNRELEASED DRAFT]',
        '--draft',
    )

    state.conf.memory_seed_loaders['draft-changelog'].append(
        MemoryLoader(
            base=[],
            description=(
                '[tox-towncrier] Print out the Towncrier-managed change '
                'notes draft for the next release to stdout'
            ),
            deps=['towncrier'],
            allowlist_externals=['sh'],
            commands_pre=[],
            commands=[
                shlex_join(
                    (
                        'sh',
                        '-c',
                        f'2>/dev/null {shlex_join(draft_inner_cmd)}',
                    ),
                ),
            ],
            commands_post=[],
            package='skip',
            skip_install='true',
        ),
    )
