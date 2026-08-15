# OpenQuatt Home Assistant

Home Assistant companion voor [OpenQuatt](https://github.com/OpenQuatt/OpenQuatt).
Deze repository is de primaire bron voor de OpenQuatt-dashboards en optionele
Home Assistant-packages. De firmware en het entity/API-contract blijven in de
firmware-repository.

## Snel starten

1. Volg [de installatiehandleiding](docs/installation.md).
2. Kies het dashboard voor je opstelling:
   - [Single · Nederlands](dashboards/single-nl.yaml)
   - [Single · Engels](dashboards/single-en.yaml)
   - [Duo · Nederlands](dashboards/duo-nl.yaml)
   - [Duo · Engels](dashboards/duo-en.yaml)
3. Lees [Dashboard gebruiken](docs/dashboard.md) voor dagelijkse controle en
   diagnose.

## Optionele packages

- [Dynamische bronselectie](docs/dynamic-sources.md)
- [Dynamische koelbronnen](docs/cooling.md)

De packages zijn optioneel. Zonder package werken de normale OpenQuatt-entiteiten
en dashboards nog steeds.

## Versies en compatibiliteit

Deze companion krijgt eigen releases, los van firmware-releases. Een release
vermeldt met welke minimale OpenQuatt- en Home Assistant-versies hij is getest.
Tot de eerste release is `main` gekoppeld aan de actuele `dev`-lijn van OpenQuatt.

Wijzigingen aan het Home Assistant entity/API-contract worden in de
[OpenQuatt-repository](https://github.com/OpenQuatt/OpenQuatt) beoordeeld op een
bijbehorende companion-wijziging. Een companion-release mag pas als compatibel
worden gemarkeerd nadat de vier dashboardvarianten en beide packages tegen dat
contract zijn gecontroleerd.

## Herkomst

De initiële dashboards, packages, documentatie en afbeeldingen zijn op
15 augustus 2026 gemigreerd uit `OpenQuatt/OpenQuatt` voor issue
[#424](https://github.com/OpenQuatt/OpenQuatt/issues/424). Oudere geschiedenis
blijft in die repository beschikbaar.

## Licentie

Dit project valt onder de [GNU General Public License v3.0](LICENSE).
