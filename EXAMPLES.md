# Exempel Automations & Templates

Här är några praktiska exempel på hur du kan använda Matilda Platform integrationen i automations och dashboards.

## Automations

### 1. Skicka meny via notifikation

```yaml
automation:
  - alias: "Skicka dagens meny varje morgon"
    description: "Skicka menyn kl 07:30 varje skoldags morgon"
    trigger:
      platform: time
      at: "07:30:00"
    condition:
      - condition: state
        entity_id: sensor.min_skola_meny_idag
        state_not: "Ingen meny idag"
      - condition: state
        entity_id: binary_sensor.workday_sensor
        state: "on"  # Bara på arbetsdagar
    action:
       - service: notify.mobile_app_min_telefon
         data:
           title: "🍽️ Dagens meny"
           message: "{{ states('sensor.min_skola_meny_idag') }}"
          data:
            channel: "meals"
            priority: "high"
```

### 2. Notifikation endast när meny ändras

```yaml
automation:
  - alias: "Notifiera när meny uppdateras"
    trigger:
      platform: state
      entity_id: sensor.min_skola_meny_idag
    condition:
      - condition: template
        value_template: "{{ trigger.to_state.state != trigger.from_state.state }}"
    action:
      - service: notify.telegram
        data:
          message: |
            Menyn har uppdaterats!
            
            {{ states('sensor.min_skola_meny_idag') }}
```

### 3. Daglig rappport med meny

```yaml
automation:
  - alias: "Daglig rapport med meny"
    trigger:
      platform: time
      at: "17:00:00"
    action:
      - service: notify.persistent_notification
        data:
          title: "📋 Daglig Rapport"
          message: |
            **Dagens Meny:**
            {{ states('sensor.min_skola_meny_idag') }}
            
            **Uppdaterad:** {{ state_attr('sensor.min_skola_meny_idag', 'last_update') }}
```

### 4. Log meny till Home Assistant logbook

```yaml
automation:
  - alias: "Logga meny varje dag"
    trigger:
      platform: time
      at: "00:00:00"
    action:
      - service: logbook.log
        data:
          name: "Matmenyer"
           message: |
             Min Skola:
             {{ states('sensor.min_skola_meny_idag') }}
```

## Templates

### Visa meny med formatering

```jinja2
{% set menu = states('sensor.min_skola_meny_idag') %}
{% if menu != 'Ingen meny idag' %}
  **Dagens meny:**
  
  {{ menu }}
{% else %}
  Ingen meny tillgänglig idag
{% endif %}
```

### Kombinera flera skolor

```jinja2
**Min Skola 1:**
{{ states('sensor.min_skola_meny_idag') }}

**Min Skola 2:**
{{ states('sensor.min_skola2_meny_idag') }}
```

### Visa senaste uppdateringstid

```jinja2
Senast uppdaterad: {{ state_attr('sensor.min_skola_meny_idag', 'last_update') | as_datetime | string }}
```

## Dashboards

### Meny Card

```yaml
type: markdown
title: "☕ Dagens Meny"
content: |
  {% if states('sensor.min_skola_meny_idag') != 'Ingen meny idag' %}
    {{ states('sensor.min_skola_meny_idag') }}
  {% else %}
    Ingen meny idag
  {% endif %}
```

### Entities Card

```yaml
type: entities
title: "Matmenyer"
entities:
  - entity: sensor.min_skola_meny_idag
    name: "Gånghesterskolan"
  - entity: sensor.min_skola_meny_idag
    name: "Skogsgläntans förskola"
```

### Custom:button-card

```yaml
type: custom:button-card
entity: sensor.min_skola_meny_idag
name: "Dagens Meny"
show_state: true
state_display: |
  [[[
    const menu = entity.state;
    if (menu === 'Ingen meny idag') {
      return 'Ingen meny';
    }
    const lines = menu.split('\n');
    return lines.length + ' rätter';
  ]]]
tap_action:
  action: fire-dom-event
  browser_mod:
    command: popup
    large: true
    content:
      type: markdown
      content: |
        {{ states('sensor.min_skola_meny_idag') }}
```

### Grid Layout

```yaml
type: grid
columns: 2
cards:
  - type: markdown
    title: "Gånghesterskolan"
    content: |
      {{ states('sensor.min_skola_meny_idag') }}
  - type: markdown
    title: "Skogsgläntans förskola"
    content: |
      {{ states('sensor.min_skola_meny_idag') }}
```

## Scripts

### Hämta och lagra meny till input_text

```yaml
script:
  save_menu_to_input:
    sequence:
      - service: input_text.set_value
        target:
          entity_id: input_text.daily_menu
        data:
          value: "{{ states('sensor.min_skola_meny_idag') }}"
```

### Skicka meny till Google Home

```yaml
script:
  announce_menu:
    sequence:
      - service: tts.google_translate_say
        data:
          entity_id: media_player.bedroom_speaker
          message: |
            Dagens meny är:
            {{ states('sensor.min_skola_meny_idag') }}
```

## Kombinationer

### Med Google Calendar

Kontrollera om det är en skoldag:

```yaml
automation:
  - alias: "Skicka meny på skoldagar"
    trigger:
      platform: time
      at: "07:30:00"
    condition:
      - condition: template
        value_template: |
          {{ 'school_day' in state_attr('calendar.min_skola', 'all_events') }}
    action:
      - service: notify.mobile_app
        data:
          message: "{{ states('sensor.min_skola_meny_idag') }}"
```

### Med template sensor

Skapa en template sensor som filtrerar vissa livsmedel:

```yaml
template:
  - sensor:
      - name: "Gluten Free Meals"
        unique_id: gluten_free_meals
        state: |
          {% set menu = states('sensor.min_skola_meny_idag') %}
          {% if 'fisk' in menu.lower() or 'kyckling' in menu.lower() %}
            Glutenfritt tillgängligt
          {% else %}
            Kontrollera med skolan
          {% endif %}
```

## Tips & Tricks

- **Använd `state_attr()`** för att få senaste uppdateringstid
- **Kombinera med `binary_sensor.workday_sensor`** för att bara skicka på arbetsdagar
- **Använd `trigger_from_state.state` och `trigger.to_state.state`** för att detektera ändringar
- **Formatera datum** med `as_datetime` filter
- **Använd `browser_mod`** för popup-visning på dashboard

## Fler exempel

Se Home Assistant Community för fler automations och templates:
- https://community.home-assistant.io/
- https://www.home-assistant.io/docs/automation/
- https://www.home-assistant.io/docs/templates/
