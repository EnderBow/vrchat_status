# VRChat Status for Home Assistant

This integration brings real-time VRChat Service Status and API Performance Statistics directly into your Home Assistant dashboard. Monitor server health, player counts, and regional networking latency to know exactly when "it's not just you" during a logout or lag spike.

## 🚀 Features

- Service Monitoring: Track the operational status of Login, Website, Networking, and SDK Uploads.

- Player Statistics: View total online users and Steam-specific player counts.

- Performance Metrics: Monitor API latency, error rates, and authentication success rates for Steam and Meta.

- Regional Health: Check the status of specific VRChat server regions (US East, US West, EU, and Japan).

- Automations: Create Home Assistant automations to notify you if VRChat services go down or if your favorite region is experiencing issues.

📊 Provided Sensors

The integration provides a wide array of sensors, including:

- sensor.vrchat_authentication_login

- sensor.vrchat_api_website

- sensor.vrchat_online_users

- sensor.vrchat_api_latency

- sensor.vrchat_usa_east_washington_d_c

- <i>(and many more)</i>

## 🎨 Dashboard Examples

To get the most out of this integration, it is recommended to use Mushroom Cards and Mini Graph Card plugins through HACS.

Example Cards:

<img width="443" height="428" alt="grafik" src="https://github.com/user-attachments/assets/d1b61959-d384-4c5d-b230-170cf7aacfa9" />

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-title-card
    title: VRChat Status
    subtitle: API / Website
  - type: grid
    columns: 2
    square: false
    cards:
      - type: custom:mushroom-template-card
        entity: sensor.vrchat_authentication_login
        primary: Login
        secondary: "{{ states(entity) | title }}"
        icon: mdi:lock
        icon_color: "{{ 'green' if is_state(entity, 'operational') else 'red' }}"
        layout: horizontal
      - type: custom:mushroom-template-card
        entity: sensor.vrchat_api_website
        primary: Website
        secondary: "{{ states(entity) | title }}"
        icon: mdi:web
        icon_color: "{{ 'green' if is_state(entity, 'operational') else 'red' }}"
        layout: horizontal
      - type: custom:mushroom-template-card
        entity: sensor.vrchat_realtime_networking
        primary: Networking
        secondary: "{{ states(entity) | title }}"
        icon: mdi:transit-connection-variant
        icon_color: "{{ 'green' if is_state(entity, 'operational') else 'red' }}"
        layout: horizontal
      - type: custom:mushroom-template-card
        entity: sensor.vrchat_realtime_player_state_changes
        primary: Player States
        secondary: "{{ states(entity) | title }}"
        icon: mdi:account-convert
        icon_color: "{{ 'green' if is_state(entity, 'operational') else 'red' }}"
        layout: horizontal
      - type: custom:mushroom-template-card
        entity: sensor.vrchat_social_friends_list
        primary: Social / Friends
        secondary: "{{ states(entity) | title }}"
        icon: mdi:account-group
        icon_color: "{{ 'green' if is_state(entity, 'operational') else 'red' }}"
        layout: horizontal
      - type: custom:mushroom-template-card
        entity: sensor.vrchat_sdk_asset_uploads
        primary: SDK Uploads
        secondary: "{{ states(entity) | title }}"
        icon: mdi:upload
        icon_color: "{{ 'green' if is_state(entity, 'operational') else 'red' }}"
        layout: horizontal
  - type: custom:mushroom-title-card
    subtitle: Realtime Networking
  - type: grid
    columns: 2
    square: false
    cards:
      - type: custom:mushroom-template-card
        entity: sensor.vrchat_usa_east_washington_d_c
        primary: USA East
        secondary: "{{ states(entity) | title }}"
        icon: mdi:map-marker
        icon_color: "{{ 'green' if is_state(entity, 'operational') else 'red' }}"
        layout: horizontal
      - type: custom:mushroom-template-card
        entity: sensor.vrchat_usa_west_san_jose
        primary: USA West
        secondary: "{{ states(entity) | title }}"
        icon: mdi:map-marker
        icon_color: "{{ 'green' if is_state(entity, 'operational') else 'red' }}"
        layout: horizontal
      - type: custom:mushroom-template-card
        entity: sensor.vrchat_europe_amsterdam
        primary: Europe
        secondary: "{{ states(entity) | title }}"
        icon: mdi:map-marker
        icon_color: "{{ 'green' if is_state(entity, 'operational') else 'red' }}"
        layout: horizontal
      - type: custom:mushroom-template-card
        entity: sensor.vrchat_japan_tokyo
        primary: Japan
        secondary: "{{ states(entity) | title }}"
        icon: mdi:map-marker
        icon_color: "{{ 'green' if is_state(entity, 'operational') else 'red' }}"
        layout: horizontal
```
