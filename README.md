[![SWUbanner]][SWUdocs]

[![tox-dev badge]][tox-dev]
[![pre-commit.ci status badge]][pre-commit.ci results page]
[![GH Sponsors badge]][GH Sponsors URL]

[SWUbanner]:
https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg
[SWUdocs]:
https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md

[tox-dev]: https://github.com/tox-dev
[tox-dev badge]:
https://img.shields.io/badge/project-yellow?label=tox-dev&labelColor=c3cc39&color=7f833e

[pre-commit.ci status badge]:
https://results.pre-commit.ci/badge/github/tox-dev/tox-towncrier/main.svg
[pre-commit.ci results page]:
https://results.pre-commit.ci/latest/github/tox-dev/tox-towncrier/main

[GH Sponsors badge]:
https://img.shields.io/badge/%40webknjaz-transparent?logo=githubsponsors&logoColor=%23EA4AAA&label=Sponsor&color=2a313c
[GH Sponsors URL]:
https://github.com/sponsors/webknjaz


# tox-towncrier

A tox plugin providing Towncrier changelog environments.


## Usage

Add `tox-towncrier` to your project's `tox` requirements -- either
in `tox.toml`:

```toml
requires = [
  "tox-towncrier",
]
```

...or in `tox.ini`:

```ini
[tox]
requires =
  tox-towncrier
```

Then invoke one of the changelog envs the plugin exposes:

```console
$ tox run -q -e draft-changelog                  # preview, never writes
$ tox run -q -e make-changelog -- 1.3.2          # cut a versioned changelog
$ tox run -q -e check-changelog                  # verify a PR has a fragment
```
