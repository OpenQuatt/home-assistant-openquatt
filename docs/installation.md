# Dashboard installeren

Op deze pagina vind je de dashboardbestanden voor OpenQuatt in Home Assistant. Volg voor een nieuwe installatie deze volgorde:

1. Rond Quick Start af via `http://openquatt.local`.
2. Voeg OpenQuatt via de ESPHome-integratie toe aan Home Assistant.
3. Installeer de twee vereiste dashboardkaarten via HACS.
4. Importeer het dashboardbestand dat bij je opstelling past.

## Welk bestand kies je?

Kies het bestand dat past bij je opstelling en voorkeurstaal:

- [Single · Nederlands](../dashboards/single-nl.yaml)
- [Single · Engels](../dashboards/single-en.yaml)
- [Duo · Nederlands](../dashboards/duo-nl.yaml)
- [Duo · Engels](../dashboards/duo-en.yaml)

Gebruik `duo` voor Duo en `single` voor Single. Kies daarna `nl` of `en`.

Open het gekozen bestand, kopieer de volledige inhoud en plak die later in de **Raw configuration editor** van Home Assistant.

## OpenQuatt via ESPHome toevoegen aan Home Assistant

OpenQuatt draait al op ESPHome-firmware. Je hoeft daarom niet eerst de ESPHome Device Builder-app in Home Assistant te installeren. De ingebouwde ESPHome-integratie is voldoende om het apparaat en alle entiteiten aan Home Assistant toe te voegen.

1. Zorg dat OpenQuatt en Home Assistant via hetzelfde netwerk bereikbaar zijn, en dat OpenQuatt niet langer dan 10 minuten geleden is herstart.
2. Open **Instellingen -> Apparaten & diensten**.
3. Staat OpenQuatt bij **Ontdekt**, kies dan **Configureren**.
4. Verschijnt OpenQuatt niet automatisch, kies **Integratie toevoegen -> ESPHome**.
5. Vul bij host `openquatt.local` of het IP-adres van OpenQuatt in. Laat de standaard API-poort `6053` staan.
6. Voer de ESPHome API-encryptiesleutel in als Home Assistant daarom vraagt. Je vindt of wijzigt die in de OpenQuatt web-app onder **Instellingen -> Systeem -> Toegang & Beveiliging**.
7. Rond de configuratie af zonder een area te selecteren.
8. Controleer bij het nieuwe OpenQuatt-apparaat of de sensoren en overige entiteiten verschijnen en waarden ontvangen.

Zie ook de officiële Home Assistant-documentatie voor de [ESPHome-integratie](https://www.home-assistant.io/integrations/esphome/).

> [!IMPORTANT]
> Selecteer bij het toevoegen van OpenQuatt nog geen Home Assistant-area. Sinds Home Assistant 2026.6 kan de area tijdens de eerste aanmaak onderdeel worden van de `entity_id`, bijvoorbeeld `sensor.zolder_openquatt_flow`. Deze dashboards gebruiken de vaste vorm `sensor.openquatt_...`. Laat de area daarom eerst leeg, wacht tot alle OpenQuatt-entiteiten zijn aangemaakt en ken daarna pas de area toe. Home Assistant wijzigt de bestaande entity-ID's dan niet meer.

## Vereiste dashboardkaarten installeren

De dashboards gebruiken twee custom dashboardkaarten die niet standaard in Home Assistant zitten:

| Dashboardkaart | Gebruikt voor |
| --- | --- |
| [Mini Graph Card](https://github.com/kalkih/mini-graph-card) | Compacte grafieken bij actuele meetwaarden |
| [ApexCharts Card](https://github.com/RomRider/apexcharts-card) | Uitgebreide temperatuur-, vermogen- en statusgrafieken |

Installeer beide kaarten bij voorkeur via [HACS](https://www.hacs.xyz/docs/use/download/download/):

1. Open **HACS** in de zijbalk van Home Assistant.
2. Zoek naar `Mini Graph Card`, open het resultaat en kies **Downloaden**.
3. Zoek naar `ApexCharts Card`, open het resultaat en kies **Downloaden**.
4. Herstart Home Assistant als HACS aangeeft dat dit nodig is.
5. Vernieuw de dashboardpagina volledig. Wis zo nodig de browsercache of herlaad de Home Assistant-app.

HACS registreert de JavaScript-resources normaal automatisch. Controleer bij problemen onder **Instellingen -> Dashboards -> menu met drie puntjes -> Resources** of deze modules aanwezig zijn:

```text
/hacsfiles/mini-graph-card/mini-graph-card-bundle.js
/hacsfiles/apexcharts-card/apexcharts-card.js
```

Zie je het menu **Resources** niet, schakel dan eerst **Geavanceerde modus** in via je Home Assistant-gebruikersprofiel.

## Dashboard importeren in Home Assistant

1. Open Home Assistant.
2. Ga naar **Instellingen -> Dashboards**.
3. Maak bij voorkeur een nieuw leeg dashboard aan of open een bestaand handmatig beheerd dashboard.
4. Open het dashboard en daarna het menu met de drie puntjes.
5. Kies **Raw configuration editor**.
6. Plak de inhoud van het gekozen YAML-bestand.
7. Sla op en laad het dashboard opnieuw.

## Bij importproblemen

- Controleer of je echt het juiste `single`- of `duo`-bestand hebt.
- Controleer of je de volledige YAML hebt geplakt.
- Controleer of de OpenQuatt-entiteiten al in Home Assistant bestaan.
- Controleer of de entity-ID's beginnen met `openquatt_` en niet met een area-prefix zoals `zolder_openquatt_`.
- Krijg je `Custom element doesn't exist: mini-graph-card` of `Custom element doesn't exist: apexcharts-card`, controleer dan of beide kaarten in HACS zijn gedownload en bij **Resources** staan.
- Zijn alleen de grafieken leeg, controleer dan onder **Ontwikkelaarstools -> Statussen** of de gebruikte `sensor.openquatt_...`-entiteiten bestaan en historie opbouwen.

### Area was al geselecteerd

Als Home Assistant de area al in de entity-ID's heeft verwerkt, zijn er twee herstelroutes:

1. Hernoem de betrokken entity-ID's in Home Assistant en verwijder alleen de area-prefix. Wijzig bijvoorbeeld `sensor.zolder_openquatt_flow` in `sensor.openquatt_flow`. De area zelf mag daarna toegewezen blijven.
2. Is dit nog een verse installatie zonder gebruikte historie of automatiseringen, verwijder OpenQuatt dan uit Home Assistant en voeg het opnieuw toe zonder area. Wacht tot de entiteiten bestaan en wijs daarna de area toe.

Pas niet de dashboard-YAML aan naar een specifieke area. Zo'n dashboard werkt dan alleen voor die ene Home Assistant-installatie.

## Optioneel: dynamische bronselectie via Home Assistant

Gebruik [dynamic-sources.yaml](../packages/dynamic-sources.yaml) alleen als je tijdens runtime zelf Home Assistant-bronnen wilt kunnen aanwijzen zonder opnieuw te flashen.

Dat pakket maakt extra helper-entiteiten aan, zoals:

- `input_text.openquatt_source_outdoor_temperature`
- `input_text.openquatt_source_water_supply_temperature`
- `input_text.openquatt_source_room_setpoint`
- `input_text.openquatt_source_room_temperature`
- `input_text.openquatt_source_heating_enable`
- `input_text.openquatt_source_cooling_enable`
- `input_text.openquatt_source_heat_demand`

Installatie in Home Assistant:

1. Zet packages aan in `/config/configuration.yaml`.
2. Kopieer het pakket naar `/config/packages/openquatt_dynamic_sources.yaml`.
3. Herlaad de template-entiteiten of herstart Home Assistant.

Vul in de helpers de entiteit in die je wilt gebruiken. Een gewone sensor ziet er zo uit:

```text
sensor.buitentemperatuur
```

Als de waarde in een attribuut van een entiteit zit, gebruik je:

```text
climate.woonkamer|current_temperature
```

De algemene dynamische bronnen publiceren stabiele proxy-entiteiten, bijvoorbeeld `sensor.openquatt_ext_outdoor_temperature`, `binary_sensor.openquatt_ext_heating_enable` en `binary_sensor.openquatt_ext_cooling_enable`. OpenQuatt kan die vervolgens als Home Assistant-bron gebruiken.

De helper `openquatt_source_heat_demand` is een uitzondering: die wijst niet naar een meting maar naar je eigen warmtevraagvoorspelling in watt. Hij vult `sensor.openquatt_ext_heat_demand`, die je in OpenQuatt kiest via `External Heat Demand Source` → `HA input`. Laat de helper leeg als je dat niet gebruikt; `Power House` rekent dan met zijn eigen huismodel.

## Optioneel: dynamische koelbronnen via Home Assistant

Gebruik [dynamic-cooling.yaml](../packages/dynamic-cooling.yaml) als je voor koeling een of meer dauwpuntbronnen vanuit Home Assistant wilt gebruiken.

Dit pakket is vooral nuttig als:

- je in meerdere kamers wilt koelen;
- je per kamer een eigen dauwpunt, temperatuur of luchtvochtigheid hebt;
- je OpenQuatt het hoogste geldige dauwpunt wilt laten gebruiken;
- je een zichtbare kamer tijdelijk niet wilt laten meetellen;
- je dauwpuntbronnen wilt aanpassen zonder opnieuw te flashen.

Installatie in Home Assistant:

1. Zet packages aan in `/config/configuration.yaml`.
2. Kopieer het pakket naar `/config/packages/openquatt_dynamic_cooling.yaml`.
3. Herlaad de template-entiteiten of herstart Home Assistant.
4. Zet `input_number.openquatt_cooling_room_count` op het aantal kamers dat je wilt gebruiken.
5. Vul per kamer de bronhelpers in.
6. Zet `input_boolean.openquatt_cooling_room_X_excluded` alleen aan voor kamers die niet moeten meetellen in de dauwpuntselectie.

Per kamer heb je twee keuzes.

Gebruik bij voorkeur een directe dauwpuntentity:

```text
sensor.woonkamer_dauwpunt
```

Vul die waarde in bij `input_text.openquatt_source_cooling_room_1_dew_point`.

Heb je geen directe dauwpuntentity, gebruik dan temperatuur plus relatieve luchtvochtigheid. Vul bijvoorbeeld `sensor.woonkamer_temperatuur` in bij `input_text.openquatt_source_cooling_room_1_temperature` en `sensor.woonkamer_luchtvochtigheid` bij `input_text.openquatt_source_cooling_room_1_humidity`:

```text
sensor.woonkamer_temperatuur
sensor.woonkamer_luchtvochtigheid
```

Ook hier mag een attribuut:

```text
climate.woonkamer|current_temperature
climate.woonkamer|current_humidity
```

Het pakket publiceert daarna:

- `sensor.openquatt_ext_cooling_dew_point`
- `binary_sensor.openquatt_ext_cooling_dew_point_valid`
- `sensor.openquatt_ha_cooling_room_1_dew_point_effective` tot en met room 6

OpenQuatt gebruikt standaard het hoogste geldige dauwpunt van kamers die niet zijn uitgesloten als veilige grens. Zet je een kamer uit via de bijbehorende `input_boolean.openquatt_cooling_room_X_excluded`, dan blijft `sensor.openquatt_ha_cooling_room_X_dew_point_effective` wel berekend, maar telt die kamer niet mee voor `sensor.openquatt_ext_cooling_dew_point`.

Met `Dauwpuntsbenadering` blijft die echte meting leidend zodra hij beschikbaar is; ontbreekt hij, dan gebruikt OpenQuatt een conservatieve benadering. Met `Expliciet toestaan` wordt de dauwpuntgrens volledig overgeslagen, ook als er wel een dauwpuntmeting beschikbaar is.

## Belangrijk om te onthouden

- De dashboards gaan uit van de entiteitsnamen uit deze repository.
- Ken de Home Assistant-area pas toe nadat de OpenQuatt-entiteiten zijn aangemaakt.
- Als je zelf entiteitsnamen wijzigt, moet je ook het dashboard aanpassen.
- Het Nederlandstalige dashboard is voor de meeste gebruikers de beste start.
- De dynamische bronpakketten zijn optioneel. Zonder package werken de normale OpenQuatt-entiteiten en dashboards nog steeds.
