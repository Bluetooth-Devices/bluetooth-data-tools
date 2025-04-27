# CHANGELOG


## v1.27.0 (2025-04-03)

### Chores

- Add gap fuzzer test ([#133](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/133),
  [`298e733`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/298e733e6185ca3e70ce9275662edb63802043ab))

### Features

- Improve performance of parsing manufacturer_data
  ([#134](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/134),
  [`f853955`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/f853955411d8c68a20fab58465b8966b76f3f21a))


## v1.26.5 (2025-04-02)

### Bug Fixes

- Reject data where the splice start position would be greater than end of the data
  ([#132](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/132),
  [`028f696`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/028f6965abd1f4d6d85fd895ad95198e74e36ca5))


## v1.26.4 (2025-04-02)

### Bug Fixes

- Add more test coverage for out of bound data
  ([#131](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/131),
  [`5249fe9`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/5249fe9374d173cf32c96c3755702f026c780457))


## v1.26.3 (2025-04-02)

### Bug Fixes

- Reduce code complexity
  ([#130](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/130),
  [`8491346`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/849134609ab511d446f24e6b596ada503ba3a23a))

### Chores

- **ci**: Bump pypa/cibuildwheel from 2.23.0 to 2.23.2 in the github-actions group
  ([#129](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/129),
  [`78a83c6`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/78a83c60ae35525ce2e3e4d1e6fe0513bab81bb9))

chore(ci): bump pypa/cibuildwheel in the github-actions group

Bumps the github-actions group with 1 update:
  [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel).

Updates `pypa/cibuildwheel` from 2.23.0 to 2.23.2 - [Release
  notes](https://github.com/pypa/cibuildwheel/releases) -
  [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md) -
  [Commits](https://github.com/pypa/cibuildwheel/compare/v2.23.0...v2.23.2)

--- updated-dependencies: - dependency-name: pypa/cibuildwheel dependency-version: 2.23.2

dependency-type: direct:production

update-type: version-update:semver-patch

dependency-group: github-actions ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#128](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/128),
  [`f28d99e`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/f28d99ec17b0643a5f032a6bf0300ce7d8051e66))

updates: - [github.com/astral-sh/ruff-pre-commit: v0.11.0 →
  v0.11.2](https://github.com/astral-sh/ruff-pre-commit/compare/v0.11.0...v0.11.2)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>


## v1.26.2 (2025-03-22)

### Bug Fixes

- Use project.license key
  ([#127](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/127),
  [`6aa523e`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/6aa523efe000a32d20f7b8e86bc48cd7251998f1))

### Chores

- **pre-commit.ci**: Pre-commit autoupdate
  ([#126](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/126),
  [`d28efe3`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/d28efe360636966287066d01c498b8607cb27596))


## v1.26.1 (2025-03-15)

### Bug Fixes

- Increase size of parse_advertisement_data_tuple cache to 1024
  ([#124](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/124),
  [`00076dc`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/00076dc4b3f51cdbfa15ef5b2a8a1dc420dccb36))

fixes #123

This one churns quite a bit and from how often its called, its a drain on performance having it so
  small.

### Chores

- Update deps ([#125](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/125),
  [`0e6492a`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/0e6492a35a3f5055b15167e15aa2e6f875fbfdc0))

- Updating coverage (7.6.10 -> 7.6.12) - Updating pytest (8.3.4 -> 8.3.5) - Updating cryptography
  (44.0.1 -> 44.0.2)

- **pre-commit.ci**: Pre-commit autoupdate
  ([#120](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/120),
  [`e45380e`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/e45380edd13e155372917a30362661e1b7686e65))


## v1.26.0 (2025-03-10)

### Features

- Reduce gap bytes slicing overhead
  ([#119](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/119),
  [`577561c`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/577561c3318f17fc02e7cdd20935290181f1b0fd))


## v1.25.1 (2025-03-05)

### Bug Fixes

- Use trusted publishing for wheel uploads
  ([#118](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/118),
  [`2bddddf`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/2bddddf888b9efe28b3ba25fefad10ccd5ff2dcb))


## v1.25.0 (2025-03-05)

### Features

- Reduce size of wheels ([#117](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/117),
  [`cc720fc`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/cc720fcc0cf6a4b68bc46895396fd32628aa1d52))


## v1.24.1 (2025-03-05)

### Bug Fixes

- Ensure Python 3.10 wheels build
  ([#116](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/116),
  [`91725a9`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/91725a9a74e3efd36f3091368179fe2cbf0b2e7d))


## v1.24.0 (2025-03-05)

### Chores

- Update release workflow for newer PSR
  ([#114](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/114),
  [`93eabee`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/93eabee3d0a0f58be29b6486a181ab3237687147))

- **ci**: Bump python-semantic-release/python-semantic-release from 9.17.0 to 9.21.0 in the
  github-actions group ([#113](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/113),
  [`bbcc3b3`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/bbcc3b3347e18119fce258ec2d9508212ec30903))

- **pre-commit.ci**: Pre-commit autoupdate
  ([#111](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/111),
  [`1a45dae`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/1a45dae9cd5bb10ced6edc306ce3f6d4274e1642))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#112](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/112),
  [`dc9f71f`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/dc9f71fff7f478b48fe3f1fd10ea53cb245e7c96))

updates: - [github.com/commitizen-tools/commitizen: v4.2.1 →
  v4.4.1](https://github.com/commitizen-tools/commitizen/compare/v4.2.1...v4.4.1) -
  [github.com/astral-sh/ruff-pre-commit: v0.9.6 →
  v0.9.9](https://github.com/astral-sh/ruff-pre-commit/compare/v0.9.6...v0.9.9)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

### Features

- Add new wheel builds ([#115](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/115),
  [`37369e8`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/37369e8f3f70e3734ad5b1912c7cab4f0a1582b6))

* feat: optimize wheel builds

Reduce size of objects

* chore: armv7l wheels


## v1.23.4 (2025-02-04)

### Bug Fixes

- Update poetry to v2 + add license to metadata
  ([#110](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/110),
  [`9cce169`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/9cce16967d35170770d8d62cb1c3d8dd66b36688))

### Chores

- **pre-commit.ci**: Pre-commit autoupdate
  ([#109](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/109),
  [`2edb0ed`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/2edb0edcd5fb75d9e440edd8298fca2f09f2b97f))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>


## v1.23.3 (2025-02-02)

### Bug Fixes

- Migrate to trusted publishing
  ([#108](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/108),
  [`38023b0`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/38023b02ee67709007d5f513131de6948df3acf3))


## v1.23.2 (2025-02-02)

### Bug Fixes

- Missing wheels ([#107](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/107),
  [`a7ace68`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/a7ace6842165e610610ebd65521548a5953bc5c4))

### Chores

- Fix CI badge ([#106](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/106),
  [`cd32f09`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/cd32f09231d2263cafe2acf249b5e88b67394756))


## v1.23.1 (2025-02-02)

### Bug Fixes

- Adjust poetry groups to fix docs build
  ([#104](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/104),
  [`b74c2bf`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/b74c2bffdc5278dc6751999ed39ec7e289cac15e))

### Build System

- **deps-dev**: Bump pytest-codspeed from 3.1.2 to 3.2.0
  ([#101](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/101),
  [`9973926`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/9973926f18fa669b06e74a332939a66baeb0ce42))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Chores

- Bump some GHA deps ([#103](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/103),
  [`85cc71f`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/85cc71f02c66f2d56c5dd3615fc95b3497736b98))

- Fix docs build ([#100](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/100),
  [`4f0903e`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/4f0903e4a226823ce341793ed9a41f3b2635b0fa))

- Update dependabot.yml to include GHA
  ([`ef9f356`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/ef9f3564f198069b4e93ecba86abc4a6f2c9ec4f))

- **ci**: Bump the github-actions group across 1 directory with 5 updates
  ([#105](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/105),
  [`268c0f4`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/268c0f46c7bd6cbfd42b748dbca27fa1817d1cc0))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>


## v1.23.0 (2025-02-02)

### Chores

- Bump upload/download actions to v4
  ([#97](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/97),
  [`82e5d05`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/82e5d0563cb4c7b407e5db5dc82bee864c052549))

- **pre-commit.ci**: Pre-commit autoupdate
  ([#96](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/96),
  [`55b134e`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/55b134e587ffbd26c57d7a1637059d01d5f8a1f5))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#98](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/98),
  [`3a6e50c`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/3a6e50ca688a2576ab897c7bc46331cfe6aed387))

### Features

- Improve cache performance
  ([#99](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/99),
  [`0dcf7ff`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/0dcf7ffba7c278bf10453c92464d8b0adcfd09d5))


## v1.22.0 (2025-01-17)

### Features

- Migrate benchmarks to use Python 3.13
  ([#95](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/95),
  [`949684e`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/949684ec43507bac7f5513c636cf7bb58222d957))


## v1.21.0 (2025-01-17)

### Build System

- **deps**: Bump cryptography from 43.0.0 to 43.0.1
  ([#69](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/69),
  [`5dec99c`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/5dec99cad1c56d7db6cf5fc489a0a000b27bd303))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump cryptography from 43.0.1 to 43.0.3 in the pip group
  ([#73](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/73),
  [`dc234ae`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/dc234ae8da9ad1eff8671c858954e7af49d7d12a))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump cryptography from 43.0.3 to 44.0.0
  ([#86](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/86),
  [`5e2b7c8`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/5e2b7c80f933e3cceb45220c923a4e13b95aa3da))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump jinja2 from 3.1.4 to 3.1.5 in the pip group
  ([#88](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/88),
  [`e1fc660`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/e1fc660567f8988cbef6530eb25c928cff7b8c0a))

- **deps**: Bump myst-parser from 1.0.0 to 3.0.1
  ([#74](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/74),
  [`02fa6ae`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/02fa6aed518c1b6a1ecc51c14eaf834ef5d9bb37))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump myst-parser from 3.0.1 to 4.0.0
  ([#89](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/89),
  [`b2cf3d4`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/b2cf3d4c04a7c6fff74b89aedb7231b80825eb95))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump sphinx from 5.3.0 to 6.2.1
  ([#65](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/65),
  [`8fdc7ca`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/8fdc7cade9c3b87dfdd77cb741d1fd83fbc154ea))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump sphinx from 6.2.1 to 7.4.7
  ([#87](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/87),
  [`ba46d70`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/ba46d700817d7fffa9c3bbc6a83593a99bc55c29))

Bumps [sphinx](https://github.com/sphinx-doc/sphinx) from 6.2.1 to 7.4.7. - [Release
  notes](https://github.com/sphinx-doc/sphinx/releases) -
  [Changelog](https://github.com/sphinx-doc/sphinx/blob/v7.4.7/CHANGES.rst) -
  [Commits](https://github.com/sphinx-doc/sphinx/compare/v6.2.1...v7.4.7)

--- updated-dependencies: - dependency-name: sphinx dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump sphinx from 7.4.7 to 8.1.3
  ([#92](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/92),
  [`2f563b2`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/2f563b236150097c94670a83c8b4e598d7d39e43))

- **deps**: Bump sphinx-rtd-theme from 1.2.0 to 2.0.0
  ([#58](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/58),
  [`e9c06db`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/e9c06db989f1a49664e83dd9fd73734e2df9904c))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump sphinx-rtd-theme from 2.0.0 to 3.0.1
  ([#75](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/75),
  [`3ab4688`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/3ab468886fc9405ba78958a28cc6d40f2cb37f93))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump sphinx-rtd-theme from 3.0.1 to 3.0.2
  ([#81](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/81),
  [`17c43a6`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/17c43a69a58e52a270f01cfc9ecba90aa24ed5c6))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest from 8.3.2 to 8.3.3
  ([#71](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/71),
  [`d0d69a5`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/d0d69a519aeb8608f6aee02b61a75fd070c852a3))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest from 8.3.3 to 8.3.4
  ([#84](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/84),
  [`93a3bdf`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/93a3bdfa8695db95784f7d8addac06ac657f9c75))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest-benchmark from 4.0.0 to 5.1.0
  ([#80](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/80),
  [`733077b`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/733077bcc040346e531a1e5e01eeed331a602426))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest-cov from 5.0.0 to 6.0.0
  ([#79](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/79),
  [`0dc38f7`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/0dc38f793247f326a16cee588034f872c7a3f95f))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Chores

- Add codspeed benchmarks ([#91](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/91),
  [`05fa2c7`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/05fa2c7a3fc29eb12e1b44d110470441f57ca738))

- **pre-commit.ci**: Pre-commit autoupdate
  ([#66](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/66),
  [`7b041ce`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/7b041ce4c82fa4545ea61a8f761d6facf8a232a0))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#67](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/67),
  [`fd49b0f`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/fd49b0fa4ef7918787b70a2d8b1191d5b879e1ea))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#70](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/70),
  [`5b0c528`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/5b0c528118f4d3984f6a3cfa7e6a15135d027b82))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#72](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/72),
  [`da219f4`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/da219f4eac7b20bc20e5d57b12e2a4eb3d95fb91))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#76](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/76),
  [`1da6085`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/1da608594010fd5c0e923fef8167e1d9d60e08ab))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#78](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/78),
  [`0ca9d53`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/0ca9d5330f4da6ef8afdbeb23756f374f4567ea8))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#82](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/82),
  [`9d1907e`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/9d1907e09285e0654f55071ace3c3a0b08f464ae))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#83](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/83),
  [`9433456`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/9433456c4b2715610769252d72ba02e07b9a0aca))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#85](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/85),
  [`7c1eb08`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/7c1eb08ddf65acaf2675d2c277a3c0544d634ff3))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#90](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/90),
  [`dbdd4a3`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/dbdd4a3e9544891e29a02d545e5ff1f5870f7952))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#93](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/93),
  [`8f4e202`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/8f4e20288fd1e76681ae9e6a1bb12c87baaef8ae))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

### Features

- Add aarch64 wheels ([#94](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/94),
  [`88d134b`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/88d134b1ac5377c515f613d5481cc35c969493e0))


## v1.20.0 (2024-08-24)

### Build System

- **deps**: Bump cryptography from 41.0.3 to 43.0.0
  ([#61](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/61),
  [`97317cc`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/97317ccbca8d7c44db8c13f0375e883b74de2685))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump myst-parser from 0.18.1 to 1.0.0
  ([#60](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/60),
  [`aa46cee`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/aa46ceef5d365c658079e06db31f90fc45f8030f))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest from 7.3.1 to 8.3.2
  ([#59](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/59),
  [`950f182`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/950f1828e3e545b02576774f2093b602e45ca6b2))

- **deps-dev**: Bump pytest-cov from 3.0.0 to 5.0.0
  ([#62](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/62),
  [`4b2d18b`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/4b2d18b5a2206f61328c78c15693c21df1404429))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Chores

- Bump deps for py3.13 ([#64](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/64),
  [`9cb11ad`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/9cb11adbaa37030c4853dc426511dbe395a3410b))

- Create dependabot.yml
  ([`f292e9a`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/f292e9a1d0162e797790c9033d69849faeb6f7fd))

- **pre-commit.ci**: Pre-commit autoupdate
  ([#54](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/54),
  [`8931368`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/8931368a38cd4e79b3c2bccbc82d6451f0690250))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#55](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/55),
  [`66b7913`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/66b79139325af943bcef6978c10566fd673eef1c))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#56](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/56),
  [`e8162e3`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/e8162e361c0a1822484205eb9b34a383552d33e4))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

### Features

- Python 3.13 support ([#57](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/57),
  [`468014e`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/468014ee5e69253eb4534013ee8cebf1ffe06c70))


## v1.19.4 (2024-07-29)

### Bug Fixes

- Speed up int_to_bluetooth_address C implementation
  ([#52](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/52),
  [`7d46575`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/7d4657515cd313aff84fee17bd027d092bd3ae3c))

### Chores

- Fix CI ([#50](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/50),
  [`434460c`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/434460ca1cbb379b0000c6f88b546ac4659df1bd))

- Fix commitlint configuration
  ([#51](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/51),
  [`7a68c25`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/7a68c2534b59a8c8bf9c2bbb40ddbbc125f69cc9))

- Make benchmarks runnable in CI
  ([#49](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/49),
  [`daac28d`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/daac28de645075625410138988832c8d0f644aea))

- Remove IDEA configuration from repository
  ([#47](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/47),
  [`3dbabf7`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/3dbabf76a0c9d07ef7baceb770f8152e8d958ece))

- Switch linting & formatting to Ruff
  ([#48](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/48),
  [`3ae1bcd`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/3ae1bcda5e65801bdadc87ab9179fbac9ab74520))

- **pre-commit.ci**: Pre-commit autoupdate
  ([#45](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/45),
  [`9a4466d`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/9a4466da63f6c8377b9ed6ccbc664813d9ff925a))

* chore(pre-commit.ci): pre-commit autoupdate

updates: - [github.com/commitizen-tools/commitizen: v2.28.0 →
  v3.27.0](https://github.com/commitizen-tools/commitizen/compare/v2.28.0...v3.27.0) -
  [github.com/pre-commit/pre-commit-hooks: v4.3.0 →
  v4.6.0](https://github.com/pre-commit/pre-commit-hooks/compare/v4.3.0...v4.6.0) -
  [github.com/pre-commit/mirrors-prettier: v2.7.1 →
  v4.0.0-alpha.8](https://github.com/pre-commit/mirrors-prettier/compare/v2.7.1...v4.0.0-alpha.8) -
  [github.com/asottile/pyupgrade: v2.37.1 →
  v3.16.0](https://github.com/asottile/pyupgrade/compare/v2.37.1...v3.16.0) -
  [github.com/PyCQA/isort: 5.12.0 → 5.13.2](https://github.com/PyCQA/isort/compare/5.12.0...5.13.2)
  - [github.com/psf/black: 22.6.0 → 24.4.2](https://github.com/psf/black/compare/22.6.0...24.4.2) -
  [github.com/codespell-project/codespell: v2.1.0 →
  v2.3.0](https://github.com/codespell-project/codespell/compare/v2.1.0...v2.3.0) -
  [github.com/PyCQA/flake8: 4.0.1 → 7.1.0](https://github.com/PyCQA/flake8/compare/4.0.1...7.1.0) -
  [github.com/pre-commit/mirrors-mypy: v0.931 →
  v1.10.1](https://github.com/pre-commit/mirrors-mypy/compare/v0.931...v1.10.1) -
  [github.com/PyCQA/bandit: 1.7.4 → 1.7.9](https://github.com/PyCQA/bandit/compare/1.7.4...1.7.9)

* chore(pre-commit.ci): auto fixes

---------

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#46](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/46),
  [`8995d2e`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/8995d2e550ffd3ade458b2b144fed7fa7b1dfc18))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>


## v1.19.3 (2024-06-24)

### Bug Fixes

- Wheel builds on macos ([#44](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/44),
  [`07f423b`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/07f423bc4ce88a357e7a06b5b48fb36dfc8b916a))


## v1.19.2 (2024-06-24)

### Bug Fixes

- Build cibuildwheel ([#43](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/43),
  [`fc8c1a1`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/fc8c1a182b189f115a687173abc20e2fe1ba2219))


## v1.19.1 (2024-06-24)

### Bug Fixes

- Fix license classifier ([#42](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/42),
  [`71d54c3`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/71d54c39e62413194a1ba65d2fe397603788e042))


## v1.19.0 (2023-12-21)

### Features

- Speed up to gap parser ([#41](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/41),
  [`595c65a`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/595c65ac0fdaac27d286c1e893abe28c8b6bfe52))


## v1.18.0 (2023-12-13)

### Features

- Add mac_to_int util ([#40](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/40),
  [`57aebfb`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/57aebfbcdf83754c8324890908d401718818d391))


## v1.17.0 (2023-12-03)

### Features

- Speed up int_to_bluetooth_address
  ([#39](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/39),
  [`ac354ae`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/ac354ae68b7afedfe5242ec50a209a6241d33169))


## v1.16.0 (2023-12-01)

### Features

- Add cython monotonic_time_coarse implementation
  ([#38](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/38),
  [`ae3abb8`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/ae3abb88023a998be5e4b75b32f0882ebb18dfd9))


## v1.15.0 (2023-11-24)

### Chores

- Add more benchmarks ([#36](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/36),
  [`0a2df27`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/0a2df279e89d0dfe381d4188321819074622f315))

### Features

- Improve performance of gap parser
  ([#37](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/37),
  [`05ea718`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/05ea718dcdf0a1d848d0eb98236439f8f0be07cf))


## v1.14.0 (2023-11-05)

### Features

- Speed up gap parser with a memory view
  ([#35](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/35),
  [`35e132f`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/35e132f30b93e964c22806c54c5d19a23fc97383))


## v1.13.0 (2023-10-18)

### Bug Fixes

- Reduce size of wheels by excluding generated .c files
  ([#34](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/34),
  [`1b56b6e`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/1b56b6e3f1579e9abb0b1d2aaf57fec39c8fc10b))

### Chores

- Add tests for esphome issue 4838
  ([#32](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/32),
  [`ddf0e58`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/ddf0e583215f79abefb23a52e42a61b08608d879))

### Features

- Update cibuildwheel to build on final cpython release
  ([#33](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/33),
  [`46781c1`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/46781c1b41eec31c5047e76a843077a3b02d6dca))


## v1.12.0 (2023-09-24)

### Features

- Small speedups to the gap parser
  ([#30](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/30),
  [`87c0fcc`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/87c0fccacde8da59b2b046fcd2e94a83f30fc364))


## v1.11.0 (2023-09-01)

### Features

- Add helper for resolving a private address using an identity key
  ([#29](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/29),
  [`b5e13cc`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/b5e13cc44711d4ef4aa306bc6e06666afde9968c))


## v1.10.0 (2023-09-01)

### Features

- Add calculate_distance_meters to estimate distance to a bluetooth device
  ([#28](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/28),
  [`c6f0150`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/c6f0150f48d73e603bf69642e7cb7b03375f8393))


## v1.9.1 (2023-08-27)

### Bug Fixes

- Rebuild wheels with cython 3.0.2
  ([#27](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/27),
  [`4634dfb`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/4634dfb8f47ab42787afecc596e864bf3ac11cbe))


## v1.9.0 (2023-08-23)

### Features

- Speed up the new parse_advertisement_data_tuple function
  ([#26](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/26),
  [`1137a50`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/1137a5004a1e2a65ee0d37ab555d6ce300208237))


## v1.8.0 (2023-08-10)

### Features

- Make returned data from parse_advertisement_data readonly
  ([#25](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/25),
  [`1a07397`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/1a073972bfc7dff35b4d8cc2d7394c4ad15f1109))


## v1.7.0 (2023-08-05)

### Build System

- Remove wheel from list of build dependencies
  ([#23](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/23),
  [`5512c3d`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/5512c3d16947c4418c544977ae46fc69810b1b64))

### Features

- Remove the need to have a cpp compiler installed
  ([#24](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/24),
  [`2a7ebac`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/2a7ebac86872407c7802a847b92ee739747cceaa))


## v1.6.1 (2023-07-24)

### Bug Fixes

- Pin python-semantic-release to fix release process
  ([#22](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/22),
  [`957ad28`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/957ad28f576c33d075f1f72875de118d5ef8fd4c))


## v1.6.0 (2023-07-13)

### Features

- Improve performance when data is all unique
  ([#21](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/21),
  [`60bff4b`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/60bff4b6f2da3cadce4305280fffc232a683122c))


## v1.5.0 (2023-07-13)

### Features

- Avoid tuple copy if data is already a tuple
  ([#20](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/20),
  [`69829ba`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/69829bae919245bd50132affb4b7718e6dffae1d))


## v1.4.0 (2023-07-13)

### Features

- Cache overall parse ([#19](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/19),
  [`5983718`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/5983718f6228e9f4428fa7843df4e37e3a7527bf))


## v1.3.0 (2023-06-29)

### Features

- Improve handling of corrupt data
  ([#18](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/18),
  [`b70fdd4`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/b70fdd45afc295b7082d8fae019e28f357356bf0))


## v1.2.0 (2023-06-15)

### Chores

- Add benchmark ([#14](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/14),
  [`46e68f4`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/46e68f427af4ee8e5b366543667814dadfd59092))

- Bump deps to fix CI ([#17](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/17),
  [`fa2e104`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/fa2e10405b4692bbeff4926744a2fdc27322beb0))

### Features

- Optimize gap parser ([#13](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/13),
  [`7df2658`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/7df26580c06cf38e2621e16a9a17a3fafb6978e4))

- Optimize gap parser ([#15](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/15),
  [`c598c2d`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/c598c2ddc106da657bfec30864a65c2e2a36c5f3))

- Optimize gap parser ([#16](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/16),
  [`5800d45`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/5800d4531400ee96f95cd4ee82677a4f32e23182))


## v1.1.0 (2023-06-14)

### Features

- Reduce string conversion overhead for bluetooth addresses
  ([#12](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/12),
  [`558c93f`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/558c93f28ffcc205df4a34be0de963fbaeddfafe))


## v1.0.0 (2023-06-07)

### Features

- Speed up parsing advertisement data
  ([#11](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/11),
  [`47e2519`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/47e251928d5d03d7978cd82f9a6173f98d0cbb68))

BREAKING CHANGE: The decode_advertisement_data function is no longer exposed

It is likely nobody was using it since it is internals for parse_advertisement_data, but it was
  exposed. If this is a problem for you, please open an issue.

### Breaking Changes

- The decode_advertisement_data function is no longer exposed


## v0.4.0 (2023-04-15)

### Features

- Add cython implementation
  ([#10](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/10),
  [`7fd349d`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/7fd349d0dd83bbcb51ade87ee8dc94fa2db67742))


## v0.3.1 (2022-12-19)

### Bug Fixes

- Handle zero padding in adv data
  ([#9](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/9),
  [`65fb26b`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/65fb26b5197d6cf1bd262eab98d52b159f89db9f))


## v0.3.0 (2022-11-13)

### Chores

- Add python 3.11 to the CI ([#8](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/8),
  [`07f114d`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/07f114df1b5f5f665001df8b681421dcf7acab1a))

- Bump python-semantic-release
  ([#7](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/7),
  [`2b4fd66`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/2b4fd668f12ac6ef4d40e0347da623e587e2058a))

### Features

- Add gap parser ([#6](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/6),
  [`dcb1d86`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/dcb1d86a15e9387385128ebaf32498d4af268963))


## v0.2.0 (2022-10-27)

### Features

- Add human_readable_name function
  ([#5](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/5),
  [`bb408cd`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/bb408cddb5f043314ec802c8b6a8a306c84fa2a3))


## v0.1.2 (2022-08-13)

### Bug Fixes

- Ci release process ([#4](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/4),
  [`1726d16`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/1726d1617ad0fceda2dee3945f12bf43768a3fe2))


## v0.1.1 (2022-08-12)

### Bug Fixes

- Release process ([#3](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/3),
  [`0a2f45b`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/0a2f45b7cba9fe71f20e2030b7712d13c330072c))


## v0.1.0 (2022-08-12)

### Chores

- Initial commit
  ([`52bb085`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/52bb0853ec9fbcc9fa6c357ff88aeb2778ccbf28))

### Features

- Add short_address ([#2](https://github.com/Bluetooth-Devices/bluetooth-data-tools/pull/2),
  [`f6eade3`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/f6eade36a4dab779d8b17a10971932ffa41f2501))

- Init repo
  ([`7a24a2d`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/7a24a2d3cc7319c85250a747fb91985e3ec3207c))
