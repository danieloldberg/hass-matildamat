# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-01

### Added
- Initial release
- Support for reading menus from Matilda Platform API
- Support for all 3500+ schools/kindergartens in Sweden
- Automatic menu updates every hour and at midnight
- Swedish and English translations
- HACS integration support
- Config flow GUI for easy setup
- Proper error handling for missing menus
- SSL certificate handling for API connections
- Debug logging for troubleshooting

### Features
- Sensor entity showing today's menu
- Attributes for distributor information
- Last update timestamp tracking
- Graceful handling of missing menu data

### Technical
- Python 3.11+ support
- Async API client
- Home Assistant 2024.1+
- aiohttp for HTTP requests

---

## Versionering

Vi använder [Semantic Versioning](https://semver.org/):
- MAJOR version för inkompatibla ändringar
- MINOR version för nya features (bakåtkompatibla)
- PATCH version för bugfixes
