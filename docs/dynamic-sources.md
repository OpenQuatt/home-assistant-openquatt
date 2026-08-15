# Dynamische bronselectie

Gebruik [dynamic-sources.yaml](../packages/dynamic-sources.yaml) als je tijdens
runtime Home Assistant-bronnen wilt aanwijzen zonder OpenQuatt opnieuw te flashen.

## Installatie

1. Zet packages aan in `/config/configuration.yaml`.
2. Kopieer het package naar `/config/packages/openquatt_dynamic_sources.yaml`.
3. Herlaad de template-entiteiten of herstart Home Assistant.

Het package maakt helpers aan voor buiten-, water- en kamertemperaturen en voor
verwarmings- en koeltoestemming. Vul een gewone bron als entity-ID in:

```text
sensor.buitentemperatuur
```

Voor een attribuut gebruik je `entity_id|attribuut`:

```text
climate.woonkamer|current_temperature
```

Het package publiceert stabiele proxy-entiteiten, waaronder
`sensor.openquatt_ext_outdoor_temperature`,
`binary_sensor.openquatt_ext_heating_enable` en
`binary_sensor.openquatt_ext_cooling_enable`. OpenQuatt kan die vervolgens als
Home Assistant-bron gebruiken.

Zie voor de volledige helperlijst en installatie-uitleg
[Dashboard installeren](installation.md#optioneel-dynamische-bronselectie-via-home-assistant).
