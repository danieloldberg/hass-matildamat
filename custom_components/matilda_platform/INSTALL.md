# Installation Guide - Matilda Platform Integration

## Steg 1: Ladda ner filerna

Integrationsmappen `MatildaPlatform/` finns här:
```
/var/folders/_k/4p09tspx3qd8k6r4jdlmplb00000gp/T/opencode/MatildaPlatform/
```

Denna mapp innehåller:
- `__init__.py` - Integrationens setup
- `const.py` - Konstanter och API endpoints
- `api.py` - API-klient
- `config_flow.py` - Konfigurationsflöde för att välja skola
- `sensor.py` - Sensor-komponenten
- `manifest.json` - Integrationens metadata
- `strings.json` - Svenska translations
- `en.json` - Engelska translations
- `README.md` - Dokumentation

## Steg 2: Installera i Home Assistant

1. **Hitta din Home Assistant config-mapp:**
   - Standard: `~/.homeassistant/` eller `/home/homeassistant/.homeassistant/`
   - Docker: `/config/` (innanför containern)
   - Home Assistant OS: Via integrationsmenu

2. **Kopiera mappen:**
   ```bash
   cp -r /var/folders/_k/4p09tspx3qd8k6r4jdlmplb00000gp/T/opencode/MatildaPlatform \
         ~/.homeassistant/custom_components/matilda_platform/
   ```

3. **Verifiera att mappen ser rätt ut:**
   ```bash
   ls -la ~/.homeassistant/custom_components/matilda_platform/
   ```
   Du bör se alla `.py`, `.json` och `.md` filer.

## Steg 3: Starta om Home Assistant

Gå till **Settings → System → Restart Home Assistant**

## Steg 4: Lägg till integrationen

1. Gå till **Settings → Devices & Services → Integrations**
2. Klicka på **Create Automation** (eller knappen för ny integration)
3. Sök efter **Matilda Platform**
4. Klicka **Create**
5. En lista med alla 3500+ skolor visas
6. Välj din skola från listan
7. Klicka **Submit**

## Steg 5: Verifiera att det fungerar

1. Gå till **Developer Tools → States**
2. Sök efter `matilda_platform` 
3. Du bör se en sensor med ditt skolnamn som innehåller dagens meny

Exempel på entity ID: `sensor.min_skola_meny_idag`

## Felsökning

### Integrationen syns inte i listan?

1. Kontrollera att mappen ligger på rätt plats:
   ```bash
   cat ~/.homeassistant/custom_components/matilda_platform/manifest.json
   ```

2. Kolla Home Assistant logs:
   - **Settings → System → Logs**
   - Sök efter "matilda_platform"

3. Lägg till debug-loggning i `configuration.yaml`:
   ```yaml
   logger:
     logs:
       custom_components.matilda_platform: debug
   ```

### Sensorn visar "Ingen meny idag"?

Det är normalt för:
- Helger och lov
- Dagar utan planerad meny
- Om menyplaneringen inte är uppdaterad i Matilda Platform

### Sensorn uppdateras inte?

1. Vänta max 1 timme (sensorn uppdateras varje timme)
2. Kolla att du har internetanslutning
3. Tvinga uppdatering: Starta om Home Assistant

## Testa lokalt innan installation

Du kan testa API:n innan du installerar:

```bash
cd /var/folders/_k/4p09tspx3qd8k6r4jdlmplb00000gp/T/opencode
python3 test_api.py
```

## Nästa steg: Automatisering

Nu kan du skapa automatisering baserat på menyn. Exempel:

### Skicka meny via notifikation

```yaml
automation:
  - alias: "Skicka dagens meny"
    trigger:
      platform: time
      at: "07:30:00"
    action:
      service: notify.mobile_app_din_telefon
      data:
        title: "Dagens meny"
        message: "{{ states('sensor.min_skola_meny_idag') }}"
```

### Dashboard med meny

Lägg till en Markdown-card:

```yaml
type: markdown
title: "Dagens meny"
content: |
  {{ states('sensor.min_skola_meny_idag') }}
```

## Support

För fler information, se `README.md` i integrationsmappen.
