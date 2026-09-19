# Setup Checklist för GitHub & HACS

Använd denna checklista för att snabbt komma igång med GitHub och HACS.

## ✅ Steg 1: GitHub Repository Setup

- [ ] **Skapa GitHub konto** om du inte har ett (https://github.com)
- [ ] **Skapa nytt repository**
  - Namn: `matilda-platform-ha`
  - Description: "Home Assistant integration for Matilda Platform school menus"
  - Public: JA
  - Initialize with README: NEJ (vi har redan en)
  - License: MIT
  - .gitignore: Python

## ✅ Steg 2: Byt alla "yourusername" referenser

Ersätt `yourusername` överallt med ditt GitHub username:

```bash
# Sök efter alla förekomster
grep -r "yourusername" .

# Ersätt (macOS/Linux)
sed -i 's/yourusername/your_actual_username/g' README.md
sed -i 's/yourusername/your_actual_username/g' hacs.json
sed -i 's/yourusername/your_actual_username/g' setup.py
sed -i 's/yourusername/your_actual_username/g' CONTRIBUTING.md
sed -i 's/yourusername/your_actual_username/g' GITHUB_SETUP.md
```

## ✅ Steg 3: Uppdatera Author Information

Redigera dessa filer och lägg in din info:

**setup.py:**
```python
author="Your Name",
author_email="your.email@example.com",
```

**pyproject.toml:**
```toml
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
```

**manifest.json:**
```json
"codeowners": ["@your_github_username"],
```

## ✅ Steg 4: Pusha till GitHub

```bash
# Från mappen matilda-platform-hacs/

# Initialisera git
git init
git add .
git commit -m "Initial commit: Matilda Platform Home Assistant integration

- Läser matmenyer från Matilda Platform API
- Stödjer 3500+ svenska förskolor och skolor
- Automatisk uppdatering varje timme
- HACS-kompatibel integration"

# Lägg till remote (byt yourusername)
git remote add origin https://github.com/yourusername/matilda-platform-ha.git

# Pusha
git branch -M main
git push -u origin main
```

## ✅ Steg 5: Skapa första Release

**Via GitHub GUI:**
1. Gå till ditt repository
2. Klick "Releases" i höger sidebar
3. Klick "Create a new release"
4. **Tag version:** `v1.0.0`
5. **Release title:** `Matilda Platform v1.0.0 - Initial Release`
6. **Description:**
   ```markdown
   ## 🎉 Initial Release

   First stable release of Matilda Platform integration for Home Assistant.

   ### Features
   - Read menus from Matilda Platform API
   - Support for 3500+ Swedish schools
   - Automatic updates hourly and at midnight
   - Swedish & English translations
   - HACS-ready

   ### Installation
   Add as custom repository in HACS:
   ```
   https://github.com/yourusername/matilda-platform-ha
   ```

   ### Usage
   See README.md for detailed documentation
   ```
7. Klick "Publish release"

## ✅ Steg 6: Verifiera GitHub Actions

1. Gå till ditt repository
2. Klick "Actions" tab
3. Du bör se:
   - ✅ "HACS Validation" workflow
   - ✅ "Validate with hassfest" workflow

Båda ska ha en ✅ green check mark.

Om någon är röd (❌), klick på den för att se vad som är fel.

## ✅ Steg 7: Lägg till Branch Protection (Optional)

**Settings → Branches → Add rule**
- Branch name pattern: `main`
- [x] Require a pull request before merging
- [x] Require status checks to pass before merging
  - Välj "hassfest" och "HACS validation"
- [x] Require branches to be up to date before merging

## ✅ Steg 8: Testa i Home Assistant

```
1. Home Assistant → HACS
2. Klick "⋯" → Custom repositories
3. Lägg in: https://github.com/yourusername/matilda-platform-ha
4. Category: Integration
5. Klick Create
6. Sök efter "Matilda Platform"
7. Install!
```

## ✅ Steg 9: Lägg till i HACS Default (Optional)

Om du vill att din integration ska visas i HACS default-listan:

1. Fork https://github.com/hacs/default
2. Redigera `repositories.json`
3. Lägg till din repo i rätt kategori
4. Öppna en Pull Request
5. Vänta på att HACS team granskar

Exempel entry:
```json
{
  "category": "integration",
  "description": "Home Assistant integration for reading school menus from Matilda Platform",
  "downloads": "https://github.com/yourusername/matilda-platform-ha/releases/latest/download/matilda_platform.zip",
  "documentation": "https://github.com/yourusername/matilda-platform-ha",
  "homeassistant": "2024.1",
  "iot_class": "cloud_polling",
  "name": "Matilda Platform",
  "requirements": [],
  "version": "1.0.0"
}
```

## ✅ Steg 10: Uppdatera Documentation

1. **Uppdatera README.md:**
   - Ersätt GitHub-URL med din URL
   - Lägg till custom repo instruktioner

2. **Uppdatera CONTRIBUTING.md:**
   - Ersätt GitHub-URL överallt

3. **Uppdatera EXAMPLES.md:**
   - Uppdatera entity IDs för dina testskolor

## 🎉 Du är klar!

Din HACS-kompatibla integration är live! 

### Nästa steg:

- 📢 Dela på Home Assistant Community Forum
- 🐛 Lägg till en issue tracker badge i README
- ⭐ Be användare att ställa en stjärna på GitHub
- 🔄 Planera framtida features

### Useful Resources

- [HACS Documentation](https://hacs.xyz/)
- [Home Assistant Integration Development](https://developers.home-assistant.io/docs/creating_integration_manifest)
- [Home Assistant Community](https://community.home-assistant.io/)

## Troubleshooting

### GitHub Actions misslyckas?

1. Klick på "Actions" tab
2. Klick på misslyckat workflow
3. Se felmeddelandet
4. Ofta är det:
   - Manifest.json syntax error
   - Saknad hacs.json
   - Import errors i Python

### HACS validering misslyckas?

```bash
# Kör lokalt
pip install hacs-cli
hacs-cli validate
```

Se output för exakt felmeddelande.

### Kan inte pusha till GitHub?

```bash
# Autentisering med token (rekommenderat)
git remote set-url origin https://token@github.com/yourusername/matilda-platform-ha.git

# Eller SSH (om SSH är konfigurerat)
git remote set-url origin git@github.com:yourusername/matilda-platform-ha.git
```

---

**Lycka till! 🚀**
