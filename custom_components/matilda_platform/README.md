# Matilda Platform Integration

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

Integrationen skapar en sensor för varje skola du lägger till:

- **Sensor ID:** `sensor.<skolnamn>_meny_idag`
- **State:** Visar dagens meny med en rad per rätt
- **Uppdateringsfrekvens:** Varje timme, plus automatisk uppdatering kl 00:00

### Exempel på output

```
• Stekta köttbullar med makaroner
• Auberginegryta med bulgur & yoghurttopping
```

## Användarscenarios

### Automation: Skicka meny via notifikation

```yaml
automation:
  - alias: "Send menu to Telegram"
    trigger:
      platform: time
      at: "07:00:00"
    action:
      service: notify.telegram
      data:
        message: "Dagens meny:\n{{ state_attr('sensor.min_skola_meny_idag', 'native_value') }}"
```

### Dashboard: Visa meny

Lägg till en Markdown-card på din dashboard:

```yaml
type: markdown
content: |
  ## Dagens meny
  {{ state_attr('sensor.min_skola_meny_idag', 'native_value') }}
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
