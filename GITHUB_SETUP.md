# GitHub Setup Instructions

För att göra detta till ett fullt HACS-kompatibelt repository behöver du:

## 1. Skapa ett GitHub Repository

```bash
# Initialisera git
cd matilda-platform-hacs
git init
git add .
git commit -m "Initial commit: Matilda Platform integration"

# Lägg till remote (byt yourusername)
git remote add origin https://github.com/yourusername/matilda-platform-ha.git
git branch -M main
git push -u origin main
```

## 2. Repository Settings

Gå till GitHub → Settings:

- [x] **Public** repository
- [x] **Require a pull request before merging**
- [x] **Require status checks to pass**
- [x] **Require branches to be up to date before merging**

## 3. Create a Release

```bash
# Tag a release
git tag v1.0.0
git push origin v1.0.0
```

Eller via GitHub GUI:
1. Go to Releases
2. Click "Create a new release"
3. Tag: `v1.0.0`
4. Title: `Matilda Platform v1.0.0`
5. Publish release

## 4. Add to HACS Default List (Optional)

1. Fork https://github.com/hacs/default
2. Add your repo to `repositories.json`
3. Submit a PR

HACS kommer att automatiskt validera din integration!

## 5. Verify HACS Compliance

Kör lokalt:

```bash
pip install hacs-cli
hacs-cli validate
```

Din integration är redo för HACS! ✅
