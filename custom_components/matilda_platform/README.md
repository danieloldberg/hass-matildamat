# Matilda Platform Integration

> **⚠️ AI-Generated** — This integration was created by an AI assistant. It works, but is new and untested in production. Report issues on GitHub.

En Home Assistant custom integration för att läsa matmenyer från Matilda Platform för svenska förskolor och skolor.

## Funktioner

- ✅ Läser meny från Matilda Platform API
- ✅ Stödjer alla skolor/förskolor som är registrerade i Matilda Platform
- ✅ Uppdaterar meny vid midnatt automatiskt
- ✅ Visar alla rätter för dagen
- ✅ Visar "Ingen meny idag" om ingen meny är tillgänglig
- ✅ Stödjer svenska och engelska

## Installation

### 1. Ladda ner integrationsmappen

Kopiera mappen `matilda_platform` till:
```
<config_directory>/custom_components/matilda_platform/
```

Där `<config_directory>` är din Home Assistant konfigurationsmapp (vanligtvis `~/.homeassistant/` eller `/home/homeassistant/.homeassistant/`).

### 2. Starta om Home Assistant

Gå till **Settings → System → Restart Home Assistant**

### 3. Lägg till integrationen

1. Gå till **Settings → Devices & Services → Create Automation**
2. Sök efter **Matilda Platform**
3. Klicka **Create**
4. Välj din skola från listan
5. Klicka **Submit**

## Hur den fungerar

Integrationen skapar sensorer för varje skola du lägger till:

**Summary Sensor:**
- **Sensor ID:** `sensor.<skolnamn>_meny_idag`
- **State:** Alla måltider för dagen
- **Attribut:** Komplett JSON-struktur med alla måltider och rätter

**Individual Meal Sensors (en per måltid):**
- **Sensor ID:** `sensor.<skolnamn>_<maaltid>` (t.ex. `sensor.<skolnamn>_lunch`)
- **State:** Rätter för denna måltid
- **Attribut:** Måltidsnamn, rättlista, mm

**Uppdateringsfrekvens:** Varje timme, plus automatisk uppdatering kl 00:00

### Exempel på output

**Summary sensor state:**
```
**Frukost:**
• Müsli
• Frukt

**Lunch:**
• Stekta köttbullar
• Potatis

**Mellanmål:**
• Frukt
```

**Individual sensor state (lunch):**
```
• Stekta köttbullar
• Potatis
```

## Användarscenarios

### Automation: Skicka all info på morgonen

```yaml
automation:
  - alias: "Send full menu to Telegram"
    trigger:
      platform: time
      at: "07:00:00"
    action:
      service: notify.telegram
      data:
        message: "{{ states('sensor.min_skola_meny_idag') }}"
```

### Automation: Avisering vid specifik rätt

```yaml
automation:
  - alias: "Alert if nuts on menu"
    trigger:
      platform: state
      entity_id: sensor.min_skola_lunch
    condition:
      - condition: template
        value_template: "{{ 'Nötter' in state_attr('sensor.min_skola_lunch', 'courses') | default([]) }}"
    action:
      service: notify.telegram
      data:
        message: "⚠️ Nötter serveras på lunch idag!"
```

### Dashboard: Komplett överblick

Lägg till Summary-sensorn för all info:

```yaml
type: markdown
content: |
  ## Dagens meny
  {{ states('sensor.min_skola_meny_idag') }}
```

### Dashboard: Separata kort för varje måltid

```yaml
type: grid
columns: 3
cards:
  - type: markdown
    title: "☕ Frukost"
    content: "{{ states('sensor.min_skola_frukost') | default('Ingen meny') }}"
  
  - type: markdown
    title: "🍽️ Lunch"
    content: "{{ states('sensor.min_skola_lunch') | default('Ingen meny') }}"
  
  - type: markdown
    title: "🍪 Mellanmål"
    content: "{{ states('sensor.min_skola_mellanmal') | default('Ingen meny') }}"
```

## Felsökning

### Sensorn visar "Kunde inte läsa in meny"

1. Kontrollera att du har internetanslutning
2. Verifiera att skolans ID är korrekt i integrationskonfigurationen
3. Kolla Home Assistant logs: **Settings → System → Logs**

### Sensorn uppdateras inte

1. Vänta en timme (sensorn uppdateras varje timme + vid midnatt)
2. Tvinga uppdatering manuellt genom att starta om Home Assistant
3. Kontrollera att API inte är nere (test på https://menu.matildaplatform.com/api/distributors)

## Skolors ID:n

För att lägga till flera skolor behöver du deras distributor ID. Du kan hitta alla tillgängliga skolor via:

```
https://menu.matildaplatform.com/api/distributors
```

Alla 3500+ skolor/förskolor finns på:
https://menu.matildaplatform.com/api/distributors

## Utveckling

### Filstruktur

```
matilda_platform/
├── __init__.py           # Integrationens main setup
├── const.py              # Konstanter och API endpoints
├── api.py                # API-klient för Matilda Platform
├── config_flow.py        # Konfigurationsflöde (GUI för val av skola)
├── sensor.py             # Sensor-komponenten (meny-sensorn)
├── manifest.json         # Integrationens metadata
├── strings.json          # Svenska translations
├── en.json               # Engelska translations
└── README.md             # Denna fil
```

### Loggning

För att se detaljerade logs, lägg till detta i `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.matilda_platform: debug
```

## Licens

MIT License

## Bidrag

Bidrag är välkomna! Skapa en GitHub issue eller pull request.
