# Historische Quatt-gegevens exporteren voor OpenQuatt

Met deze tool exporteer je historische energiegegevens uit de Quatt-cloud via Home Assistant. De export bevat per dag onder andere het elektriciteitsverbruik en de warmteproductie van de warmtepomp en ketel.

De exporter maakt twee bestanden:

- een **JSON-bestand** voor import in de OpenQuatt web-app;
- een **CSV-bestand** voor controle of verdere verwerking, bijvoorbeeld in een spreadsheet.

Deze tool is vooral bedoeld voor een **eenmalige historische import**. Er wordt geen automatische of doorlopende synchronisatie ingesteld.

> [!IMPORTANT]
> De exporter gebruikt de niet-officiële, reverse-engineerde Quatt Remote API. De werking kan veranderen wanneer Quatt of de gebruikte Home Assistant-integratie wordt aangepast.

## In het kort

1. Controleer of de Quatt-integratie in Home Assistant werkt en de **Remote API** is ingeschakeld.
2. Installeer en configureer **Pyscript**.
3. Kopieer het Python-bestand naar `/config/pyscript/`.
4. Voeg het meegeleverde Home Assistant-script toe.
5. Herstart Home Assistant.
6. Start de export met een begin- en einddatum.
7. Download het JSON-bestand en importeer het in OpenQuatt.

## Benodigd

- Een werkende Home Assistant-installatie.
- De niet-officiële [`home-assistant-quatt`](https://github.com/marcoboers/home-assistant-quatt)-integratie.
- Een geconfigureerde Quatt CiC met ingeschakelde **Remote API**.
- De Home Assistant-action `quatt.get_cic_insights`.
- [HACS](https://www.hacs.xyz/) met de integratie [Pyscript](https://github.com/custom-components/pyscript).
- Toegang tot de Home Assistant-configuratiemap `/config`.

De voorbeeldbestanden in deze map zijn:

- [`openquatt_quatt_insights_export.py`](openquatt_quatt_insights_export.py): de Pyscript-service die Quatt-gegevens ophaalt en JSON/CSV schrijft;
- [`openquatt_quatt_insights_export.yaml`](openquatt_quatt_insights_export.yaml): een eenvoudig Home Assistant-script om de export te starten.

## 1. Controleer de Quatt Remote API

De export gebruikt historische gegevens uit de Quatt-cloud. Alleen de lokale CiC-koppeling is daarom niet voldoende; de **Remote API** moet zijn ingeschakeld.

Voor een bestaande Quatt-integratie:

1. Open in Home Assistant **Instellingen → Apparaten & diensten → Integraties**.
2. Open de Quatt-integratie en kies **Configureren**.
3. Schakel **Add Remote API** in.
4. Meld je aan bij de Quatt mobiele API.
5. Druk, wanneer daarom wordt gevraagd, binnen 60 seconden op de fysieke knop van de Quatt CiC.

Controleer daarna of de benodigde action beschikbaar is:

1. Open **Ontwikkelaarstools → Acties**.
2. Zoek naar `quatt.get_cic_insights`.

Verschijnt deze action niet, controleer dan of:

- de Remote API werkelijk is ingeschakeld;
- de Quatt-integratie opnieuw is geladen;
- Home Assistant na de installatie of update opnieuw is gestart;
- je een recente versie van `home-assistant-quatt` gebruikt.

Meer informatie staat in de documentatie van [`home-assistant-quatt`](https://github.com/marcoboers/home-assistant-quatt#remote-mobile-api).

## 2. Installeer en configureer Pyscript

Installeer Pyscript via HACS:

1. Open **HACS → Integraties**.
2. Zoek naar **Pyscript**.
3. Installeer de integratie.
4. Herstart Home Assistant.
5. Open **Instellingen → Apparaten & diensten**.
6. Voeg de integratie **Pyscript** toe.

Gebruik bij het configureren van Pyscript deze instellingen:

- **Allow All Imports?**: aan;
- **Access hass as a global variable?**: uit;
- **Use legacy decorators?**: uit.

`Allow All Imports?` is nodig omdat de exporter normale Python-modules zoals `json`, `csv`, `os` en `tempfile` gebruikt om bestanden te schrijven.

> [!CAUTION]
> Met **Allow All Imports** mag Pyscript-code normale Python-modules gebruiken. Plaats daarom alleen Pyscript-bestanden uit een bron die je vertrouwt.

## 3. Installeer het Python-bestand

1. Download [`openquatt_quatt_insights_export.py`](openquatt_quatt_insights_export.py).
2. Kopieer het bestand naar:

   ```text
   /config/pyscript/openquatt_quatt_insights_export.py
   ```

3. Maak de map `/config/pyscript` aan wanneer deze nog niet bestaat.
4. Controleer dat de bestandsnaam exact gelijk is aan `openquatt_quatt_insights_export.py`.

## 4. Voeg het Home Assistant-script toe

### Aanbevolen: via `scripts.yaml`

1. Open [`openquatt_quatt_insights_export.yaml`](openquatt_quatt_insights_export.yaml).
2. Kopieer alleen het blok **onder** de bovenste regel `script:`.
3. Plak dat blok op hoofdniveau in:

   ```text
   /config/scripts.yaml
   ```

Voeg dus niet nogmaals een bovenste `script:`-regel toe aan `scripts.yaml`.

Het resultaat moet naast eventueel bestaande scripts staan, bijvoorbeeld:

```yaml
bestaand_script:
  alias: Bestaand script
  sequence: []

openquatt_export_quatt_insights_daily:
  alias: OpenQuatt export Quatt insights daily
  # De overige regels uit het voorbeeldbestand volgen hier.
```

### Alternatief: als Home Assistant-package

Gebruik je al Home Assistant-packages, kopieer dan het volledige bestand [`openquatt_quatt_insights_export.yaml`](openquatt_quatt_insights_export.yaml) naar je package-map.

Gebruik de `scripts.yaml`-methode wanneer je niet zeker weet of packages in jouw Home Assistant-configuratie zijn ingeschakeld.

## 5. Herstart en controleer Home Assistant

Herstart Home Assistant nadat beide bestanden zijn geplaatst. Daarmee worden zowel Pyscript als de Home Assistant-scripts opnieuw geladen.

Controleer daarna onder **Ontwikkelaarstools → Acties** of beide actions bestaan:

```text
pyscript.openquatt_export_quatt_insights
script.openquatt_export_quatt_insights_daily
```

Ontbreekt alleen de `pyscript.`-action, controleer dan het Python-bestand en de Pyscript-configuratie.

Ontbreekt alleen de `script.`-action, controleer dan het YAML-bestand, de inspringing en de plaatsing in `scripts.yaml` of je package-map.

## 6. Maak een export

Open in Home Assistant **Ontwikkelaarstools → Acties** en voer het voorbeeldscript uit:

```yaml
action: script.openquatt_export_quatt_insights_daily
data:
  from_date: "2024-01-01"
  to_date: "2024-01-31"
```

De begin- en einddatum worden allebei meegenomen.

- `from_date`: eerste dag die je wilt exporteren;
- `to_date`: laatste dag die je wilt exporteren;
- wanneer `to_date` leeg blijft, gebruikt het voorbeeldscript de datum van vandaag;
- wanneer `from_date` leeg blijft, gebruikt het huidige voorbeeldscript `2024-01-01`.

Vul `from_date` daarom bij voorkeur altijd expliciet in, bijvoorbeeld met de installatiedatum van je Quatt of de eerste datum waarvoor OpenQuatt-historie ontbreekt.

Er is geen automation nodig voor een eenmalige import.

### Wat gebeurt er tijdens de export?

De standaard dag-export haalt de gegevens per kalendermaand op:

```yaml
timeframe: month
daily: true
daily_source: month
advanced_insights: true
```

De Quatt-maandresponse bevat afzonderlijke dagregels. De exporter combineert deze regels tot één JSON-bestand met alle gevraagde dagen.

Daardoor wordt normaal gesproken slechts **één Quatt API-call per kalendermaand** gedaan, in plaats van één call per dag. Tussen opeenvolgende maandcalls zit standaard 750 ms.

Start niet meerdere exports tegelijk met dezelfde bestandsnaam.

## 7. Controleer het resultaat

De bestanden worden standaard geschreven naar:

```text
/config/www/openquatt-insights/openquatt-quatt-insights-daily-<from>-<to>.json
/config/www/openquatt-insights/openquatt-quatt-insights-daily-<from>-<to>.csv
```

Via de Home Assistant-webserver zijn ze bereikbaar via:

```text
/local/openquatt-insights/openquatt-quatt-insights-daily-<from>-<to>.json
/local/openquatt-insights/openquatt-quatt-insights-daily-<from>-<to>.csv
```

Voor het voorbeeld van 1 tot en met 31 januari 2024 wordt de JSON-URL dus:

```text
https://<jouw-home-assistant-adres>/local/openquatt-insights/openquatt-quatt-insights-daily-2024-01-01-2024-01-31.json
```

Je kunt het resultaat ook controleren via **Ontwikkelaarstools → Statussen**. Zoek daar naar:

```text
pyscript.openquatt_quatt_insights_export
```

De attributen van deze status bevatten onder andere:

- `json_path`: locatie van het JSON-bestand;
- `csv_path`: locatie van het CSV-bestand;
- `json_url`: downloadpad via `/local`;
- `csv_url`: downloadpad via `/local`;
- `day_count`: aantal geëxporteerde dagen;
- `missing_day_count`: aantal dagen waarvoor Quatt geen volledige dagregel teruggaf;
- `sample_count`: aantal geëxporteerde regels.

Bij een fout wordt geen succesvol leeg exportbestand opgeslagen. Controleer in dat geval de Home Assistant-logboeken.

## 8. Importeer het bestand in OpenQuatt

Gebruik bij voorkeur het JSON-bestand:

1. Download het gegenereerde `.json`-bestand.
2. Open de OpenQuatt web-app.
3. Ga naar **Instellingen → Gegevens bewaren → Resultaten**.
4. Open het onderdeel **Historie importeren**.
5. Kies **Bestand kiezen**.
6. Selecteer het JSON-bestand.
7. Controleer het importoverzicht en start de import.

De Quatt-cloudexport bevat dagtotalen. Een export die rechtstreeks vanuit een OpenQuatt-device wordt gemaakt kan daarnaast ook uurdetail bevatten.

CSV kan eveneens door OpenQuatt worden geïmporteerd, maar JSON is het aanbevolen formaat voor overdracht en herstel van OpenQuatt-energiehistorie.

## Privacy en beveiliging

> [!WARNING]
> Bestanden onder `/config/www` zijn via `/local` bereikbaar zonder Home Assistant-authenticatie voor clients die de Home Assistant-webserver kunnen bereiken. Dit kan ook gelden via je externe Home Assistant-adres.

Daarom:

- deel de `/local`-URL niet publiek;
- laat `include_raw: false` staan, tenzij je de volledige oorspronkelijke Quatt-response bewust nodig hebt;
- verwijder de exportbestanden na de import wanneer je ze niet meer nodig hebt;
- gebruik desgewenst een andere schrijfbare map wanneer downloaden via `/local` niet nodig is.

## Ontbrekende dagen

Het JSON-bestand bevat een veld `missing_days`. Daarin staan dagen binnen het gevraagde bereik waarvoor Quatt geen volledige dagregel met minimaal warmtepompverbruik en warmtepompopbrengst heeft teruggegeven.

Toekomstige dagen worden niet als ontbrekend gemarkeerd en leiden niet tot cloudcalls.

Een beperkt aantal ontbrekende dagen kan betekenen dat Quatt voor die periode geen bruikbare historische gegevens beschikbaar heeft. Quatt ververst CiC-insights ongeveer eenmaal per uur; zeer recente gegevens kunnen daarom nog onvolledig zijn.

## Problemen oplossen

| Probleem of foutmelding | Controle of oplossing |
|---|---|
| `quatt.get_cic_insights` bestaat niet | Schakel de Quatt Remote API in, update de Quatt-integratie en herstart of herlaad de integratie. |
| `Home Assistant service quatt.get_cic_insights is not available` | De benodigde Quatt-action is niet geregistreerd. Controleer de Remote API en de versie van `home-assistant-quatt`. |
| `No remote connection available` | De Quatt Remote API is niet actief of de aanmelding is niet meer geldig. Configureer de Remote API opnieuw. |
| `pyscript.openquatt_export_quatt_insights` bestaat niet | Controleer of het Python-bestand in `/config/pyscript/` staat en herstart of herlaad Pyscript. |
| Fout bij `json`, `csv`, `os` of `tempfile` | Zet bij Pyscript **Allow All Imports?** aan. |
| `script.openquatt_export_quatt_insights_daily` bestaat niet | Controleer de plaatsing en inspringing van het YAML-blok en herlaad de scripts. |
| `output_dir must be an absolute path` | Gebruik een volledig pad dat met `/` begint, bijvoorbeeld `/config/www/openquatt-insights`. |
| `Permission denied` | Kies een map waarin het Home Assistant-proces bestanden mag maken. |
| De `/local/...`-URL geeft een 404 | Controleer of het bestand werkelijk onder `/config/www/` staat en of de bestandsnaam en datums exact overeenkomen. |
| Veel dagen staan in `missing_days` | Controleer het datumbereik en of Quatt voor die dagen historische gegevens toont. |
| De maximale API-calllimiet wordt overschreden | Splits de periode in meerdere kleinere exports. |
| De export lijkt van de verkeerde installatie te komen | Zie de beperking voor meerdere CiCs hieronder. |

## Belangrijke beperkingen

### Reverse-engineerde API

De gebruikte Quatt-cloud-API is reverse-engineered en biedt geen gegarandeerde achterwaartse compatibiliteit. Een wijziging in `home-assistant-quatt` of aan Quatt-zijde kan een update van de exporter nodig maken.

### Meerdere Quatt CiCs

De exporter heeft momenteel geen keuzeveld voor een specifieke Quatt-installatie. Wanneer meerdere CiCs met Remote API in dezelfde Home Assistant-installatie zijn geconfigureerd, gebruikt de Quatt-action de eerste beschikbare remote CiC-koppeling.

Controleer in dat geval vóór de OpenQuatt-import zorgvuldig of de export van de juiste installatie afkomstig is.

### Limiet op het aantal cloudcalls

Om te voorkomen dat een foutief datumbereik onbeperkt API-calls uitvoert, accepteert één export maximaal:

- 120 maandcalls bij `daily_source: month`;
- 366 dagcalls bij `daily_source: day`.

Splits een grotere periode in meerdere exports.

## Geavanceerd: de Pyscript-service rechtstreeks aanroepen

Voor normaal gebruik is het meegeleverde Home Assistant-script voldoende. Gevorderde gebruikers kunnen de Pyscript-service ook rechtstreeks aanroepen:

```yaml
action: pyscript.openquatt_export_quatt_insights
data:
  from_date: "2024-01-01"
  to_date: "2024-01-31"
  timeframe: month
  daily: true
  daily_source: month
  advanced_insights: true
  output_dir: /config/www/openquatt-insights
  base_name: openquatt-quatt-insights-daily-2024-01-01-2024-01-31
  include_raw: false
  day_delay_ms: 750
  local_timezone: Europe/Amsterdam
```

### Belangrijkste opties

| Optie | Betekenis |
|---|---|
| `from_date` | Eerste dag van de export in `YYYY-MM-DD`-formaat. |
| `to_date` | Laatste dag van de dag-export. Leeg betekent vandaag. |
| `daily` | `true` maakt het OpenQuatt-dagformaat voor energiehistorie. |
| `daily_source` | Gebruik normaal `month`; `day` is alleen een fallback. |
| `output_dir` | Absolute map waarin JSON en CSV worden geschreven. |
| `base_name` | Bestandsnaam zonder `.json` of `.csv`. |
| `include_raw` | Voegt de volledige Quatt-response toe aan JSON. Normaal uit laten. |
| `day_delay_ms` | Pauze tussen opeenvolgende Quatt API-calls, standaard 750 ms. |
| `local_timezone` | Tijdzone waarmee UTC-tijdstippen aan lokale kalenderdagen worden gekoppeld. |

Met `daily: false` kan de service ook een genormaliseerde analyse-export voor één Quatt-timeframe maken. Die gebruikt het schema `openquatt.quatt_insights.v1` en is **niet** bedoeld voor de OpenQuatt-energiehistorie-import.

`daily_source: day` haalt elke dag afzonderlijk op. Dat veroorzaakt één API-call per dag en is daarom alleen bedoeld als fallback. Gebruik normaal `daily_source: month`.

## Bestandsformaat

De dag-export gebruikt het schema:

```text
openquatt.quatt_insights_daily.v1
```

Een vereenvoudigd JSON-voorbeeld:

```json
{
  "schema": "openquatt.quatt_insights_daily.v1",
  "query": {
    "timeframe": "month",
    "daily_source": "month"
  },
  "missing_days": [],
  "days": [
    {
      "date": "2024-01-01",
      "energy_hp_electric": 0,
      "energy_hp_heat": 0,
      "energy_boiler_heat": 0
    }
  ]
}
```

Belangrijke velden en eenheden:

| Veld | Betekenis | Eenheid |
|---|---|---|
| `date` | Kalenderdag | `YYYY-MM-DD` |
| `energy_hp_electric` | Elektriciteitsverbruik van de warmtepomp | Wh |
| `energy_hp_heat` | Warmteproductie van de warmtepomp | Wh |
| `energy_boiler_heat` | Warmteproductie van de ketel | Wh |

Wanneer `include_raw: true` wordt gebruikt, kan een dag daarnaast een `raw_sample` bevatten.

Een export die rechtstreeks vanuit de OpenQuatt web-app wordt gemaakt gebruikt hetzelfde JSON-schema, maar kan aanvullende velden bevatten, zoals:

- `energy_hp_cooling`: koelafgifte van de warmtepomp in Wh;
- `heating_input_wh`: elektrisch verbruik dat aan verwarmen is toegewezen in Wh;
- `cooling_input_wh`: elektrisch verbruik dat aan koelen is toegewezen in Wh.

`system_heat_output_wh` wordt niet geëxporteerd. De systeemwarmte is afleidbaar uit `energy_hp_heat` plus `energy_boiler_heat`.

De CSV bevat dezelfde dagregels als een platte tabel.

## Waarom Pyscript en niet `python_script`?

De ingebouwde Home Assistant-integratie `python_script` draait in een beperkte sandbox en ondersteunt geen normale Python-imports. Dat is voldoende voor kleine helpers die bijvoorbeeld een Home Assistant-sensor vullen, maar niet geschikt voor deze exporter.

Deze exporter schrijft volledige JSON- en CSV-bestanden en gebruikt daarvoor modules zoals `json`, `csv`, `os` en `tempfile`. Pyscript is daarvoor praktischer.

De bestanden worden eerst volledig tijdelijk geschreven en daarna per bestand vervangen. Zo blijft bij een schrijffout niet eenvoudig een gedeeltelijk overschreven exportbestand achter.

## Bijwerken

Vervang bij een update zowel:

- `openquatt_quatt_insights_export.py`;
- het gebruikte scriptblok uit `openquatt_quatt_insights_export.yaml`.

Herstart Home Assistant of herlaad daarna zowel Pyscript als de Home Assistant-scripts.
