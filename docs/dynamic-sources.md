# Dynamische bronselectie

Gebruik [dynamic-sources.yaml](../packages/dynamic-sources.yaml) als je tijdens
runtime Home Assistant-bronnen wilt aanwijzen zonder OpenQuatt opnieuw te flashen.

## Installatie

1. Zet packages aan in `/config/configuration.yaml`.
2. Kopieer het package naar `/config/packages/openquatt_dynamic_sources.yaml`.
3. Herlaad de template-entiteiten of herstart Home Assistant.

Het package maakt helpers aan voor buiten-, water- en kamertemperaturen, voor
verwarmings- en koeltoestemming, en voor een optionele externe warmtevraag en
een optioneel aanvoertarget. Vul een gewone bron als entity-ID in:

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

De helper `openquatt_source_heating_supply_target` wijst naar een gewenst
aanvoertarget in graden Celsius. Hij vult
`sensor.openquatt_ext_heating_supply_target`; de bijbehorende
`binary_sensor.openquatt_ext_heating_supply_target_valid` staat alleen aan bij
een numerieke waarde van 20 tot en met 70 °C. Kies in OpenQuatt
`Heating Supply Target Source` → `HA input` om dit target te gebruiken. Laat de
helper leeg om de eigen stooklijn te blijven gebruiken.

Het package controleert de proxy's iedere 15 seconden. Daarnaast publiceert het
een centrale heartbeat (`sensor.openquatt_ha_ingress_heartbeat`) waarvan de
state zelf ongeveer eenmaal per minuut verandert. Daardoor kan OpenQuatt een
werkende Home Assistant-koppeling onderscheiden van een bevroren verbinding,
ook als een proxywaarde urenlang gelijk blijft: een constante waarde blijft
bruikbaar zolang de heartbeat binnenkomt. Bij een ongeldige bron schakelt het
validiteitssignaal uit en valt OpenQuatt terug op de stooklijn.

Zie voor de volledige helperlijst en installatie-uitleg
[Dashboard installeren](installation.md#optioneel-dynamische-bronselectie-via-home-assistant).
