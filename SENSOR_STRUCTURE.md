# Sensor Structure - Option 1+2

## Overview

The integration creates **two types of sensors**:

1. **Summary Sensor** (Option 2) - Complete daily menu in one sensor
2. **Individual Meal Sensors** (Option 1) - One sensor per meal type

This hybrid approach provides maximum flexibility for both simple dashboards and advanced automations.

## Summary Sensor

**Entity ID:** `sensor.<school_name>_meny_idag`

**Example:** `sensor.min_skola_meny_idag`

### State

Formatted text of all meals and courses:

```
**Frukost:**
• Müsli
• Frukt

**Lunch:**
• Stekta köttbullar
• Potatis
• Bönor

**Mellanmål:**
• Frukt
• Mjölk
```

### Attributes

- `meals` - Complete JSON structure:
  ```json
  [
    {
      "name": "Frukost",
      "courses": ["Müsli", "Frukt"]
    },
    {
      "name": "Lunch",
      "courses": ["Stekta köttbullar", "Potatis", "Bönor"]
    }
  ]
  ```
- `meal_count` - Number: 3
- `distributor_id` - School ID
- `distributor_name` - School name
- `last_update` - ISO timestamp

### Use Cases

- Dashboards with complete daily menu overview
- Notifications with all meals at once
- Automations checking multiple meals
- Accessing raw JSON via attributes for advanced templates

## Individual Meal Sensors

**Entity ID pattern:** `sensor.<school_name>_<meal_name>`

**Examples:**
- `sensor.min_skola_frukost`
- `sensor.min_skola_lunch`
- `sensor.min_skola_mellanmal`
- `sensor.min_skola_frukt_och_ka` (auto-generated safe names)

### State

Text with only courses for this meal:

```
• Stekta köttbullar
• Potatis
• Bönor
```

### Attributes

- `courses` - List of courses:
  ```json
  ["Stekta köttbullar", "Potatis", "Bönor"]
  ```
- `meal_name` - String: "Lunch"
- `distributor_id` - School ID
- `distributor_name` - School name
- `last_update` - ISO timestamp

### Use Cases

- Drag individual meals onto dashboard
- Trigger automations on specific meal
- Create alerts for allergen detection
- Separate notifications per meal

## Dynamic Meal Discovery

Meal names are **auto-discovered** from the API response. If a school has:
- Only "Lunch" → 2 sensors created (1 summary + 1 meal)
- "Frukost", "Lunch", "Mellanmål" → 4 sensors (1 summary + 3 meals)
- Custom meal names → Sensors adapt automatically

Meal names are slugified for entity IDs:
- "Frukost" → `sensor.school_frukost`
- "Mellanmål" → `sensor.school_mellanmal`
- "Frukt & Kaka" → `sensor.school_frukt_kaka`

## Update Frequency

Both sensor types update on the same schedule:
- Every hour (configurable)
- Automatically at midnight (00:00)

## Templates & Automations

### Example: Check if meal exists

```jinja2
{% if states('sensor.min_skola_lunch') != 'Ingen meny idag' %}
  Lunch is available
{% endif %}
```

### Example: Access courses as list

```jinja2
{% set courses = state_attr('sensor.min_skola_lunch', 'courses') or [] %}
{% for course in courses %}
  - {{ course }}
{% endfor %}
```

### Example: Check for allergen

```jinja2
{% set courses = state_attr('sensor.min_skola_lunch', 'courses') or [] %}
{% if 'Mjölk' in courses %}
  ⚠️ Dairy in lunch today!
{% endif %}
```

### Example: Get all meals from summary

```jinja2
{% set meals = state_attr('sensor.min_skola_meny_idag', 'meals') or [] %}
Meals today: {{ meals | length }}
```

## No Data Scenarios

When no menu data is available:

- **Summary sensor state:** "Ingen meny idag"
- **Individual sensor states:** "Ingen meny idag"
- **Summary attributes:** `meals = []`, `meal_count = 0`
- **Individual attributes:** `courses = []`

## Technical Details

- Sensors are created once during `async_setup_entry()`
- Meal names remain consistent across updates (no re-creation)
- API response is parsed once per update cycle
- Both sensor types use identical update mechanism
- If API fails: state = "Kunde inte läsa in meny"
