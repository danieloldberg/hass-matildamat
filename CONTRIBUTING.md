# Bidra till Matilda Platform Integration

Tack för att du är intresserad av att bidra! Här är riktlinjer för hur du kan hjälpa.

## Code of Conduct

Vi förväntar oss ett respektfullt och inkluderande beteende från alla bidragsgivare.

## Hur man bidrar

### Rapportera bugs

1. Kontrollera att buggen inte redan är rapporterad
2. Öppna en [GitHub Issue](https://github.com/yourusername/matilda-platform-ha/issues/new?template=bug_report.yml)
3. Inkludera:
   - Version av integrationen
   - Version av Home Assistant
   - Steg för att återskapa
   - Relevanta logs

### Föreslå features

1. Öppna en [GitHub Issue](https://github.com/yourusername/matilda-platform-ha/issues/new?template=feature_request.yml)
2. Beskriv:
   - Vad funktionen ska göra
   - Varför det behövs
   - Eventuella alternativa lösningar

### Skicka kod

1. **Forka repositoriet**
   ```bash
   git clone https://github.com/yourusername/matilda-platform-ha.git
   cd matilda-platform-ha
   ```

2. **Skapa en feature branch**
   ```bash
   git checkout -b feature/my-amazing-feature
   ```

3. **Installera dev dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements-dev.txt
   ```

4. **Gör dina ändringar**
   - Kod ska följa PEP 8
   - Lägg till docstrings
   - Inkludera tests om möjligt

5. **Format och lint**
   ```bash
   black custom_components/matilda_platform/
   isort custom_components/matilda_platform/
   flake8 custom_components/matilda_platform/
   ```

6. **Kör tests**
   ```bash
   pytest
   ```

7. **Commit dina ändringar**
   ```bash
   git commit -m "Add: descriptive commit message"
   ```

8. **Pusha till din fork**
   ```bash
   git push origin feature/my-amazing-feature
   ```

9. **Öppna en Pull Request**
   - Beskriv vad du har gjort
   - Länka till relaterade issues
   - Se till att alla checks passerar

## Commit messages

Använd följande format för commit messages:

- `Add:` - Ny feature
- `Fix:` - Buggfix
- `Refactor:` - Kodförbättring
- `Docs:` - Dokumentation
- `Tests:` - Test-relaterade ändringar

Exempel:
```
Add: Support for multiple schools in single config entry
Fix: Handle missing menu data gracefully
Docs: Update README with examples
```

## Pull Request Process

1. Uppdatera README.md om du har gjort ändringar i functionality
2. Uppdatera version numbers enligt SemVer
3. Säkerställ att alla GitHub workflows passerar
4. En eller flera maintainers kommer att granska din PR
5. Möjliga ändringar kan behövas innan merge

## Kodstandard

- Python 3.11+
- Type hints där möjligt
- Docstrings för alla functions
- Tydliga variabelnamn
- Kommentarer för komplex logik

## Testing

Alla nya features och bugfixes bör ha tests:

```python
async def test_my_new_feature():
    """Test my new feature."""
    # Arrange
    api = MatildaPlatformAPI(session)
    
    # Act
    result = await api.get_menu("test-id")
    
    # Assert
    assert result is not None
```

## Filer du behöver veta om

- `custom_components/matilda_platform/__init__.py` - Integration setup
- `custom_components/matilda_platform/sensor.py` - Sensor implementation
- `custom_components/matilda_platform/api.py` - API client
- `custom_components/matilda_platform/config_flow.py` - Configuration UI
- `custom_components/matilda_platform/strings.json` - Translations

## Support

- 📧 Issues: https://github.com/yourusername/matilda-platform-ha/issues
- 💬 Discussions: https://github.com/yourusername/matilda-platform-ha/discussions
- 🏠 Home Assistant Community: https://community.home-assistant.io

Tack för dina bidrag! ❤️
