# Quick Start Guide

## Installation (5 minuter)

### 1. Lägg till Custom Repository i HACS

```
https://github.com/yourusername/matilda-platform-ha
```

**Steg:**
1. Home Assistant → HACS → Integrations
2. Klick på tre prickar (⋯) → Custom repositories
3. Klistra in URL:en ovan
4. Välj **Integration** som category
5. Klick **Create**

### 2. Installera integrationen

1. HACS → Integrations
2. Sök: "Matilda Platform"
3. Klick **Install**
4. Starta om Home Assistant

### 3. Lägg till din skola

1. Settings → Devices & Services → Integrations
2. Klick **Create**
3. Sök: "Matilda Platform"
4. Välj din skola från listan
5. Klick **Submit**

**Det är klart!** 🎉

En sensor har skapats: `sensor.<skolnamn>_meny_idag`

## Verifiera

### Hitta sensorn

1. Developer Tools → States
2. Sök efter `matilda_platform`
3. Du bör se din sensors state

### Läsa menyn

**Template:**
```jinja2
{{ states('sensor.min_skola_meny_idag') }}
```

**Output:**
```
• Stekta köttbullar med makaroner
• Auberginegryta med bulgur & yoghurttopping
```

## Nästa steg

### Skicka notifikation

```yaml
automation:
  - alias: "Skicka meny varje morgon"
    trigger:
      at: "07:30:00"
      platform: time
    action:
      service: notify.mobile_app_din_telefon
      data:
        title: "Dagens meny"
        message: "{{ states('sensor.min_skola_meny_idag') }}"
```

### Lägg till på dashboard

**Markdown Card:**
```yaml
type: markdown
title: "☕ Dagens Meny"
content: |
  {{ states('sensor.min_skola_meny_idag') }}
```

## Felsökning

### Sensorn syns inte?

```bash
# Kolla manuell installation
ls ~/.homeassistant/custom_components/matilda_platform/
```

### Ingen meny?

Kolla Home Assistant logs (Settings → System → Logs):
```
custom_components.matilda_platform
```

### Uppdateras inte?

- Sensorn uppdateras varje timme
- Tvinga: Starta om Home Assistant

## Slut!

Du är klar! Njut av digitala matmenyer i Home Assistant! 🍴
