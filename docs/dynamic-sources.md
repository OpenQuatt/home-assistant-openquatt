# Dynamische bronselectie

Gebruik [dynamic-sources.yaml](../packages/dynamic-sources.yaml) als je tijdens
runtime Home Assistant-bronnen wilt aanwijzen zonder OpenQuatt opnieuw te flashen.

## Installatie

1. Zet packages aan in `/config/configuration.yaml`.
2. Kopieer het package naar `/config/packages/openquatt_dynamic_sources.yaml`.
3. Herlaad de template-entiteiten of herstart Home Assistant.

Het package maakt helpers aan voor buiten-, water- en kamertemperaturen, voor
verwarmings- en koeltoestemming, en voor een optionele externe warmtevraag. Vul
een gewone bron als entity-ID in:

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

De helper `openquatt_source_heat_demand` is optioneel en wijst naar je eigen
warmtevraagvoorspelling in watt. Hij vult `sensor.openquatt_ext_heat_demand`,
die `Power House` als feedforward kan gebruiken in plaats van zijn eigen
huismodel. Laat hem leeg als je dat niet wilt.

Zie voor de volledige helperlijst en installatie-uitleg
[Dashboard installeren](installation.md#optioneel-dynamische-bronselectie-via-home-assistant).
