# Changelog

<!--next-version-placeholder-->

## v1.8.0 (2023-08-10)

### Feature

* Make returned data from parse_advertisement_data readonly ([#25](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/25)) ([`1a07397`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/1a073972bfc7dff35b4d8cc2d7394c4ad15f1109))

## v1.7.0 (2023-08-05)

### Feature

* Remove the need to have a cpp compiler installed ([#24](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/24)) ([`2a7ebac`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/2a7ebac86872407c7802a847b92ee739747cceaa))

## v1.6.1 (2023-07-24)

### Fix

* Pin python-semantic-release to fix release process ([#22](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/22)) ([`957ad28`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/957ad28f576c33d075f1f72875de118d5ef8fd4c))

## v1.6.0 (2023-07-13)

### Feature

* Improve performance when data is all unique ([#21](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/21)) ([`60bff4b`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/60bff4b6f2da3cadce4305280fffc232a683122c))

## v1.5.0 (2023-07-13)

### Feature

* Avoid tuple copy if data is already a tuple ([#20](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/20)) ([`69829ba`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/69829bae919245bd50132affb4b7718e6dffae1d))

## v1.4.0 (2023-07-13)

### Feature

* Cache overall parse ([#19](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/19)) ([`5983718`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/5983718f6228e9f4428fa7843df4e37e3a7527bf))

## v1.3.0 (2023-06-29)

### Feature

* Improve handling of corrupt data ([#18](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/18)) ([`b70fdd4`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/b70fdd45afc295b7082d8fae019e28f357356bf0))

## v1.2.0 (2023-06-15)

### Feature

* Optimize gap parser ([#16](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/16)) ([`5800d45`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/5800d4531400ee96f95cd4ee82677a4f32e23182))
* Optimize gap parser ([#15](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/15)) ([`c598c2d`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/c598c2ddc106da657bfec30864a65c2e2a36c5f3))
* Optimize gap parser ([#13](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/13)) ([`7df2658`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/7df26580c06cf38e2621e16a9a17a3fafb6978e4))

## v1.1.0 (2023-06-14)
### Feature
* Reduce string conversion overhead for bluetooth addresses ([#12](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/12)) ([`558c93f`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/558c93f28ffcc205df4a34be0de963fbaeddfafe))

## v1.0.0 (2023-06-07)
### Feature
* Speed up parsing advertisement data ([#11](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/11)) ([`47e2519`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/47e251928d5d03d7978cd82f9a6173f98d0cbb68))

### Breaking
* The decode_advertisement_data function is no longer exposed ([`47e2519`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/47e251928d5d03d7978cd82f9a6173f98d0cbb68))

## v0.4.0 (2023-04-15)
### Feature
* Add cython implementation ([#10](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/10)) ([`7fd349d`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/7fd349d0dd83bbcb51ade87ee8dc94fa2db67742))

## v0.3.1 (2022-12-19)
### Fix
* Handle zero padding in adv data ([#9](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/9)) ([`65fb26b`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/65fb26b5197d6cf1bd262eab98d52b159f89db9f))

## v0.3.0 (2022-11-13)
### Feature
* Add gap parser ([#6](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/6)) ([`dcb1d86`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/dcb1d86a15e9387385128ebaf32498d4af268963))

## v0.2.0 (2022-10-27)
### Feature
* Add human_readable_name function ([#5](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/5)) ([`bb408cd`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/bb408cddb5f043314ec802c8b6a8a306c84fa2a3))

## v0.1.2 (2022-08-13)
### Fix
* Ci release process ([#4](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/4)) ([`1726d16`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/1726d1617ad0fceda2dee3945f12bf43768a3fe2))

## v0.1.1 (2022-08-12)
### Fix
* Release process ([#3](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/3)) ([`0a2f45b`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/0a2f45b7cba9fe71f20e2030b7712d13c330072c))

## v0.1.0 (2022-08-12)
### Feature
* Add short_address ([#2](https://github.com/Bluetooth-Devices/bluetooth-data-tools/issues/2)) ([`f6eade3`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/f6eade36a4dab779d8b17a10971932ffa41f2501))
* Init repo ([`7a24a2d`](https://github.com/Bluetooth-Devices/bluetooth-data-tools/commit/7a24a2d3cc7319c85250a747fb91985e3ec3207c))
