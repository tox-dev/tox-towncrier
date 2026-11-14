# Naming the Ducks

Canonical names for this project, and how to refer to it in
prose. Other files in `.agents-ctx/` (and any generated content)
should say "the project" rather than hardcoding one of these --
reach for a specific name only when the distinction actually
matters (e.g. citing a package, an import, or a repository URL).

## Distribution / PyPI name: `tox-towncrier`

The installable, published name -- recorded in
`pyproject.toml`'s `[project].name` per PEP 621. This is also
the preferred way to refer to the project by name in prose.

## Python import name: `tox_plugins.towncrier`

The plugin lives in the `tox_plugins` PEP 420 implicit namespace
package, shared with other `tox_plugins.*` distributions. Nothing
outside tox imports it directly: tox finds it through the
`tox-towncrier` entry point in the `tox` group, declared in
`pyproject.toml`'s `[project.entry-points.tox]`.

## GitHub repository slug: `tox-dev/tox-towncrier`

Use it verbatim when it's actually the repository being
referenced (URLs, `gh` invocations, PR/issue citations) -- not as
a stand-in for the project's name in prose.

## Don't say bare `towncrier`

`towncrier` on its own is the upstream changelog tool the plugin
wraps, not this project. The plugin provides the
`make-changelog`, `check-changelog`, and `draft-changelog` tox
envs that run it. Say which one is meant -- e.g. "the
`make-changelog` tox env", "the Towncrier tool" -- and say
`tox-towncrier` for this project.
