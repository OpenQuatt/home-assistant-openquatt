# Dynamische koelbronnen

Gebruik [dynamic-cooling.yaml](../packages/dynamic-cooling.yaml) als je voor
koeling een of meer dauwpuntbronnen uit Home Assistant wilt gebruiken.

## Installatie

1. Zet packages aan in `/config/configuration.yaml`.
2. Kopieer het package naar `/config/packages/openquatt_dynamic_cooling.yaml`.
3. Herlaad de template-entiteiten of herstart Home Assistant.
4. Zet `input_number.openquatt_cooling_room_count` op het aantal kamers.
5. Vul per kamer een dauwpuntbron of temperatuur plus luchtvochtigheid in.
6. Zet `input_boolean.openquatt_cooling_room_X_excluded` alleen aan voor kamers
   die niet moeten meetellen.

Gebruik bij voorkeur een directe dauwpuntentity:

```text
sensor.woonkamer_dauwpunt
```

Heb je geen directe bron, vul dan temperatuur en relatieve luchtvochtigheid in:

```text
sensor.woonkamer_temperatuur
sensor.woonkamer_luchtvochtigheid
```

Ook attributen zijn toegestaan:

```text
climate.woonkamer|current_temperature
climate.woonkamer|current_humidity
```

Het package publiceert:

- `sensor.openquatt_ext_cooling_dew_point`
- `binary_sensor.openquatt_ext_cooling_dew_point_valid`
- `sensor.openquatt_ha_cooling_room_1_dew_point_effective` tot en met room 6

OpenQuatt gebruikt het hoogste geldige dauwpunt van niet-uitgesloten kamers als
veilige grens. Met `Dauwpuntsbenadering` blijft een echte meting leidend zodra die
beschikbaar is. Met `Expliciet toestaan` wordt de dauwpuntgrens volledig
overgeslagen; gebruik dat alleen als je het condensrisico bewust beheert.

Zie voor de volledige helperlijst en installatie-uitleg
[Dashboard installeren](installation.md#optioneel-dynamische-koelbronnen-via-home-assistant).
