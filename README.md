# RadiaCode 101 sensor component

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

**DEPRECATED**: i cannot get it to stable. Replaced with MQTT publisher: https://github.com/cdump/radiacode/pull/6 .


**This component will set up the following platforms.**

| Platform | Description                                    |
| -------- | ---------------------------------------------- |
| `sensor` | Show info from RadiaCode 101 Radiation sensor. |

This integration uses https://github.com/cdump/radiacode library. Kudos to Maxim!

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `radiacode_bt`.
4. Download _all_ the files from the `custom_components/radiacode_bt/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "RadiaCode 101"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/radiacode_bt/__init__.py
custom_components/radiacode_bt/config_flow.py
custom_components/radiacode_bt/const.py
custom_components/radiacode_bt/manifest.json
custom_components/radiacode_bt/sensor.py
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

---

[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/vooon/hass-radiacode.svg?style=for-the-badge
[commits]: https://github.com/vooon/hass-radiacode/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/vooon/hass-radiacode.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40vooon-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/vooon/hass-radiacode.svg?style=for-the-badge
[releases]: https://github.com/vooon/hass-radiacode/releases
[user_profile]: https://github.com/vooon
