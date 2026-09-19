# Example Home Assistant Configuration

Här är ett fullständigt exempel på hur du kan konfigurера Matilda Platform integrationen tillsammans med automations och dashboards.

## configuration.yaml

```yaml
# Example configuration.yaml

homeassistant:
  name: "Min Hem"
  unit_system: metric
  time_zone: "Europe/Stockholm"

# Integrations
http:

api:

frontend:

automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml

# Logger
logger:
  default: info
  logs:
    custom_components.matilda_platform: debug

# Input helpers för att lagra data
input_text:
  daily_menu:
    name: "Dagens Meny"
    icon: mdi:food

# Notifications
notify:
  - platform: mobile_app
```

## automations.yaml

```yaml
# Skicka meny varje morgon
- alias: "Skicka dagens meny"
  description: "Skicka menyn kl 07:30 på skoldagar"
  id: "send_daily_menu"
  trigger:
    platform: time
    at: "07:30:00"
  condition:
    - condition: state
      entity_id: sensor.min_skola_meny_idag
      state_not: "Ingen meny idag"
  action:
    - service: notify.mobile_app_min_telefon
      data:
        title: "🍽️ Dagens meny"
        message: |
          Min Skola:
          {{ states('sensor.min_skola_meny_idag') }}
        data:
          channel: "meals"
    - service: input_text.set_value
      target:
        entity_id: input_text.daily_menu
      data:
        value: "{{ states('sensor.min_skola_meny_idag') }}"

# Uppdaterad notifikation
- alias: "Notifiera när meny ändras"
  description: "Skicka alert när menyn uppdateras"
  id: "menu_updated_notification"
  trigger:
    platform: state
    entity_id: sensor.min_skola_meny_idag
  condition:
    - condition: template
      value_template: "{{ trigger.to_state.state != trigger.from_state.state }}"
  action:
    - service: persistent_notification.create
      data:
        title: "Meny Uppdaterad"
        message: |
          {{ states('sensor.min_skola_meny_idag') }}
        notification_id: "menu_update"
```

## ui-lovelace.yaml (Dashboard)

```yaml
title: "Home"
views:
  - path: "default_view"
    title: "Hem"
    cards:
      - type: heading
        heading: "Skolans Meny"

      - type: markdown
        title: "☕ Min Skola"
        content: |
          {% if states('sensor.min_skola_meny_idag') != 'Ingen meny idag' %}
            {{ states('sensor.min_skola_meny_idag') }}
          {% else %}
            Ingen meny idag
          {% endif %}

      - type: markdown
        title: "🍴 Min Skola"
        content: |
          {% if states('sensor.min_skola_meny_idag') != 'Ingen meny idag' %}
            {{ states('sensor.min_skola_meny_idag') }}
          {% else %}
            Ingen meny idag
          {% endif %}

      - type: entities
        title: "Senaste Uppdateringar"
        entities:
          - entity: sensor.min_skola_meny_idag
            name: "Min Skola"
          - entity: sensor.min_skola_meny_idag
            name: "Min Skola"
```

## scripts.yaml

```yaml
# Spara meny till file
save_menu:
  sequence:
    - service: python_script.write_file
      data:
        file: "/config/www/menu.txt"
        content: |
          Min Skola:
          {{ states('sensor.min_skola_meny_idag') }}

# Skicka meny via Telegram
send_to_telegram:
  sequence:
    - service: notify.telegram
      data:
        message: |
          🍽️ Dagens Meny
          
          Min Skola:
          {{ states('sensor.min_skola_meny_idag') }}
          
          Min Skola:
          {{ states('sensor.min_skola_meny_idag') }}
```

## Filstruktur

```
~/.homeassistant/
├── configuration.yaml
├── automations.yaml
├── scripts.yaml
├── scenes.yaml
├── custom_components/
│   └── matilda_platform/
│       ├── __init__.py
│       ├── api.py
│       ├── const.py
│       ├── config_flow.py
│       ├── sensor.py
│       ├── manifest.json
│       ├── strings.json
│       └── en.json
└── www/
    └── menu.txt
```

## Installation Steps

1. **Installera integration** (se README.md)
2. **Kopiera automations.yaml** ovan till din config
3. **Kopiera dashboard-cards** från ui-lovelace.yaml
4. **Starta om** Home Assistant
5. **Verifiera** att sensorer visas i Developer Tools → States

## Testa

```bash
# Se logs
tail -f /var/log/homeassistant/home-assistant.log | grep matilda_platform

# eller via HA UI
# Settings → System → Logs → custom_components.matilda_platform
```

Allt klart! 🎉
