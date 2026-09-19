# Repository Structure

Här är den kompletta strukturen för Matilda Platform HACS integrationen:

```
matilda-platform-ha/                          # Root repository
│
├── .github/
│   ├── workflows/
│   │   ├── hassfest.yml                       # Validerar med Home Assistant hassfest
│   │   └── hacs.yml                           # Validerar med HACS
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml                     # Template för bug reports
│   │   └── feature_request.yml                # Template för feature requests
│   └── pull_request_template.md               # PR template
│
├── custom_components/
│   └── matilda_platform/                      # Integration folder (REQUIRED by HACS)
│       ├── __init__.py                        # Integration setup & scheduling
│       ├── api.py                             # Matilda Platform API client
│       ├── const.py                           # Constants & config keys
│       ├── config_flow.py                     # GUI for selecting school
│       ├── sensor.py                          # Menu sensor entity
│       ├── manifest.json                      # Integration metadata
│       ├── strings.json                       # Swedish translations
│       ├── en.json                            # English translations
│       ├── INSTALL.md                         # Installation guide
│       ├── README.md                          # Integration documentation
│       └── test_matilda.py                    # Test script
│
├── .gitignore                                 # Git ignore rules
├── LICENSE                                    # MIT License
├── README.md                                  # Main project README
├── QUICKSTART.md                              # Quick start guide (5 min setup)
├── EXAMPLES.md                                # Usage examples & templates
├── CONTRIBUTING.md                            # Contribution guidelines
├── CHANGELOG.md                               # Version history
├── CONFIG_EXAMPLE.md                          # Example HA configuration
├── GITHUB_SETUP.md                            # GitHub setup instructions
├── hacs.json                                  # HACS metadata (REQUIRED)
├── pyproject.toml                             # Modern Python packaging
├── setup.py                                   # Setup script
├── requirements.txt                           # Python dependencies
└── requirements-dev.txt                       # Development dependencies
```

## Kritiska HACS-filer

För att integrationen ska fungera i HACS måste dessa filer finnas:

✅ `custom_components/matilda_platform/manifest.json` - Integration metadata  
✅ `hacs.json` - HACS configuration  
✅ `custom_components/matilda_platform/__init__.py` - Main integration file  
✅ `custom_components/matilda_platform/sensor.py` - Sensor platform  
✅ `README.md` - Project documentation  
✅ `LICENSE` - License file  

## Workflow-validering

Två GitHub Actions validerar automatiskt:

1. **hassfest.yml** - Home Assistant integration validation
2. **hacs.yml** - HACS compliance check

Dessa körs vid varje push och pull request.

## Filöversikt

| File | Purpose |
|------|---------|
| `manifest.json` | Integration metadata, requirements, version |
| `hacs.json` | HACS-specifika settings (name, domains, docs) |
| `api.py` | API client för Matilda Platform |
| `config_flow.py` | Config UI (välja skola) |
| `sensor.py` | Meny-sensorn |
| `const.py` | API endpoints, config keys |
| `strings.json` | Svenska translations |
| `en.json` | English translations |
| `pyproject.toml` | Modern Python packaging config |
| `setup.py` | Python package setup |

## Installation för End Users

```bash
# Via HACS (rekommenderat)
1. HACS → Integrations → Custom repositories
2. Lägg till: https://github.com/yourusername/matilda-platform-ha
3. Installera Matilda Platform

# Manuell installation
1. Kopiera custom_components/matilda_platform/ till ~/.homeassistant/custom_components/
2. Starta om Home Assistant
```

## For Developers

```bash
# Clone & setup
git clone https://github.com/yourusername/matilda-platform-ha.git
cd matilda-platform-ha
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

# Test
python3 custom_components/matilda_platform/test_matilda.py

# Validate
hacs-cli validate
```

## Documentation

- **README.md** - Main documentation
- **QUICKSTART.md** - 5-minute setup guide
- **EXAMPLES.md** - Automations, templates, dashboards
- **CONFIG_EXAMPLE.md** - Full HA configuration example
- **CONTRIBUTING.md** - How to contribute
- **GITHUB_SETUP.md** - How to set up the GitHub repo

## GitHub Repository Setup

```bash
# Initialize git
git init
git add .
git commit -m "Initial commit"

# Add remote
git remote add origin https://github.com/yourusername/matilda-platform-ha.git
git branch -M main
git push -u origin main

# Create a release
git tag v1.0.0
git push origin v1.0.0
```

## Key Features

✅ Supports 3500+ Swedish schools  
✅ Automatic menu updates (hourly + midnight)  
✅ Swedish & English translations  
✅ HACS validation workflows  
✅ Comprehensive documentation  
✅ Example automations & dashboards  
✅ MIT License  
✅ Community-ready with issue templates  

## Next Steps

1. **Create GitHub repo** - See GITHUB_SETUP.md
2. **Update usernames** - Replace "yourusername" in files
3. **Create first release** - Tag v1.0.0
4. **Add to HACS default** - Optional (see README.md)

Ready for HACS! 🚀
