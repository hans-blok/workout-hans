# Presentatie-richtlijnen – Workout Hans

**Doel**: Rustige, duidelijke presentatie van de trainingsschema's voor Hans, passend bij de workspace *workout-hans*.

---

## Basisprincipes

- **Rustig en eenvoudig**: weinig visuele ruis, veel witruimte.
- **Japans minimalisme**: zachte aardetinten, simpele vormen, geen drukke effecten.
- **B1-taal**: korte zinnen, duidelijke koppen, logische volgorde.
- **Geen inhoud wijzigen**: alleen presentatie (indeling, navigatie, stijl).

---

## Structuur van de publicatie

### Landingspagina

- Bestandsnaam: `docs/index.html`.
- Functie: startpunt voor Hans om zijn schema's te vinden.
- Bevat **tegels** (kaarten) voor:
  - Krachttraining (weekschema)
  - Tennis training (1x per week, 60 minuten)
  - Ochtend yoga & mobility (dagelijks kort ritueel)
- Elke tegel toont:
  - Een duidelijke titel met emoji (🏋️, 🎾, 🧘).
  - 1–2 korte zinnen met uitleg.
  - Een subtiele tag (bijv. "4x per week").

### Bestandslocaties

- Inhoudelijke markdown-bestanden:
  - `docs/resultaten/personal-trainer/*.md`
  - `docs/resultaten/tennis-trainer/*.md`
- Gepubliceerde HTML (Publisher output):
  - `docs/resultaten/publisher/*.html`
- `index.html` blijft in `docs/` staan (root van de publicatie).
- De landingspagina linkt naar de **Publisher-HTML** in `docs/resultaten/publisher/`.

---

## Navigatiepatroon

- Lezer start op `index.html`.
- Van daaruit kiest Hans één van de drie schema's:
  - **Krachttraining** → weekschema kracht (4x per week).
  - **Tennis training** → tennisschema (1x per week, 60 min).
  - **Ochtend mobility** → kort dagelijks ritueel na het ontbijt.
- Elke HTML-pagina van Publisher gebruikt dezelfde rustige, minimale stijl (via eenvoudige CSS).

---

## Visuele stijl

- Achtergrond: warm, licht beige (`#f4f1ea`).
- Kaarten: zacht crèmekleurig (`#fffcf8` / `#fdfbf7`).
- Lijnen en randen: dunne, subtiele grijs/beige tinten.
- Kleurenaccenten:
  - Kracht: gedempt groen/grijs (`#6b705c`).
  - Tennis: warm bruin/oranje (`#cb997e`).
  - Ochtend-mobility: zacht blauwgroen of neutrale tint (kan later worden toegevoegd indien nodig).
- Animaties: alleen lichte hover-effecten (kleine schaduw, minieme verschuiving).

---

## Patronen voor schema-overzichten

- Waar mogelijk worden oefeningen per training gepresenteerd in **tabellen**:
  - Kolommen: oefening, sets x reps / duur, notities.
  - Dit verhoogt de scanbaarheid zonder de inhoud aan te passen.
- Korte inleidingen per trainingsdag of sessie blijven boven de tabellen staan.

---

## Samenwerking met Publisher

- Publisher converteert alle `.md`-schema's naar `.html` in `docs/resultaten/publisher/`.
- Presentatie Architect zorgt dat `index.html` naar deze HTML-bestanden linkt.
- Er wordt geen inhoud in de `.md`-bestanden veranderd door deze rol; alleen de landingspagina en richtlijnen worden aangepast.

---

**Versie**: 1.0  
**Laatst bijgewerkt**: 12 januari 2026
