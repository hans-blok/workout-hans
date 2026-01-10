# Workspace Standaard voor Document-Repositories

**Versie**: 1.0  
**Datum**: 10 januari 2026  
**Status**: Bindend

---

## Doel

Dit document normeert de folderstructuur en organisatie van document-repositories. Het zorgt voor consistentie, vindbaarheid en professionaliteit over alle workspaces heen.

## Toepassingsgebied

Deze standaard geldt voor:
- Document-repositories (geen applicatie code)
- Knowledge bases
- Governance repositories
- Policy documentatie
- Procedure documentatie

Deze standaard geldt **niet** voor:
- Software ontwikkelprojecten met code
- Data repositories
- Binary asset repositories

---

## Verplichte Folderstructuur

### Niveau 1: Root Folders (Verplicht)

```
/docs                    # Alle inhoudelijke documentatie
/governance             # Gedragscode, policies, procedures, rolbeschrijvingen
/templates              # Document templates en voorbeelden
/temp                    # Tijdelijke context en voorstellen (niet in git)
/.github                # GitHub configuratie en agents
README.md               # Repository overzicht en getting started
.gitignore             # Git ignore patterns
```

#### `/docs` - Documentatie
**Doel**: Alle inhoudelijke documentatie die het primaire doel van de repository vormt.

**Structuur** (suggestie):
```
/docs
  /procedures           # Hoe-documentatie
  /policies            # Wat-documentatie
  /guidelines          # Best practices en richtlijnen
  /references          # Naslagwerk en definities
```

**Eisen**:
- Elk document in Markdown (.md) format
- Duidelijke bestandsnamen (lowercase, geen spaties, gebruik hyphens)
- Maximaal 3 niveaus diep

#### `/governance` - Governance
**Doel**: Regels, normen en structuur van de workspace zelf.

**Verplichte inhoud**:
```
/governance
  gedragscode.md        # Of link naar centrale gedragscode
  beleid.md            # Workspace-specifiek beleid met scope
  /rolbeschrijvingen   # Rolbeschrijvingen (optioneel)
```

**Optionele inhoud**:
- `agent-standaard.md` - Indien workspace agents gebruikt
- `/procedures` - Werkwijzen voor deze workspace
- `CONTRIBUTING.md` - Bijdrage richtlijnen
- `CODEOWNERS` - Verantwoordelijken per gebied

**Eisen**:
- `beleid.md` bevat minimaal: context, scope, niet-in-scope (zie Constitutie Artikel 9)
- Alle governance documenten op B1 taalniveau

#### `/templates` - Templates
**Doel**: Herbruikbare sjablonen voor nieuwe documenten.

**Voorbeelden**:
```
/templates
  document-template.md
  procedure-template.md
  policy-template.md
  meeting-notes-template.md
```

**Eisen**:
- Templates bevatten placeholders tussen `< >`
- Elk template heeft duidelijke instructies bovenaan
- Templates zelf zijn ook in Markdown

#### `/.github` - GitHub Configuratie
**Doel**: GitHub-specifieke configuratie, workflows en prompts.

**Structuur**:
```
/.github
  /prompts             # Prompt bestanden (*.prompt.md)
  /workflows           # GitHub Actions (optioneel)
  ISSUE_TEMPLATE/      # Issue templates (optioneel)
  PULL_REQUEST_TEMPLATE.md  # PR template (optioneel)
```

**Eisen**:
- Alleen technische configuratie, geen business content
- Prompt bestanden eindigen op `.prompt.md`

#### `/temp` - Tijdelijke Context
**Doel**: Workspace context, voorstellen, plannen en werk-in-uitvoering die niet in git hoort.

**Typische inhoud**:
```
/temp
  context.md           # Workspace context en scope beschrijving
  agent-voorstellen.md # Voorstellen voor benodigde agents
  notities.md          # Werk notities en ideeën
  *-plan.md            # Plannen (bijv. workspace-init-plan.md)
```

**Gebruik**:
- Context meegeven aan agents tijdens workspace opzet
- Basis voor `governance/beleid.md`
- Brainstorm voor agent definities
- Tijdelijke werk documenten
- **Plannen**: Ontwerp documenten, architectuur beslissingen, implementatie plannen

**Eisen**:
- Wordt NIET gecommit naar git (zie .gitignore)
- Vrije structuur, geen verplichte bestanden
- Markdown format aanbevolen voor leesbaarheid
- Plannen krijgen naam patroon: `{onderwerp}-plan.md`

---

## Verplichte Root Bestanden

### `README.md`
**Doel**: Eerste oriëntatiepunt voor bezoekers van de repository.

**Verplichte secties**:
1. **Titel en korte beschrijving** - Wat is dit?
2. **Structuur** - Overzicht van folders
3. **Gebruik** - Hoe gebruik je deze repository?
4. **Bijdragen** - Hoe kun je bijdragen? (indien van toepassing)
5. **Licentie** - Onder welke licentie (indien van toepassing)

**Optionele secties**:
- Quick links naar belangrijkste documenten
- Status badges
- Contact informatie

### `.gitignore`
**Verplichte uitsluitingen**:
```gitignore
# Tijdelijke context folder
/temp/

# Editor bestanden
.vscode/
.idea/
*.swp
*~

# OS bestanden
.DS_Store
Thumbs.db

# Tijdelijke bestanden
*.tmp
*.bak
*.log

# Build output (indien aanwezig)
_site/
.jekyll-cache/
```

### `LICENSE` (Optioneel)
- Alleen indien de repository publiekelijk wordt gedeeld
- Kies passende licentie (bijv. MIT, CC-BY-4.0 voor documentatie)

---

## Optionele Folders

### `/assets` - Media en Bestanden
Voor afbeeldingen, diagrammen, downloads:
```
/assets
  /images
  /diagrams
  /downloads
```

**Eisen**:
- Georganiseerd per type
- Gebruik web-vriendelijke formaten (PNG, JPG, SVG)
- Logische bestandsnamen

### `/archive` - Gearchiveerde Content
Voor oude of uitgefaseerde documenten:
```
/archive
  /yyyy-mm          # Gearchiveerd per datum
```

**Eisen**:
- Duidelijk markeren als archief in README
- Niet indexeren in hoofdnavigatie
- Bewaar alleen wat historische waarde heeft

### `/config` - Configuraties
Voor workspace-specifieke tool configuraties:
```
/config
  .vimrc
  copilot.lua
  .editorconfig
```

### `/scripts` - Agent Runners (Optioneel)
Voor uitvoerbare scripts (bijv. Python voor agent automatisering):
```
/scripts
  <script-naam>.py     # Uitvoerbaar script
  common/              # Gedeelde utilities (optioneel)
```

**Eisen**:
- Executable en gedocumenteerd
- Duidelijke usage instructies

---

## Naamgevingsconventies

### Folders
- **Lowercase**: Alleen kleine letters
- **Plural**: Meervoud voor collections (`docs`, `templates`, `policies`)
- **Hyphens**: Gebruik `-` voor meerwoordige namen (`meeting-notes`)
- **Geen spaties**: Nooit spaties in folder namen

### Bestanden
- **Lowercase**: Alleen kleine letters voor consistentie
- **Hyphens**: Gebruik `-` tussen woorden (`git-workflow.md`)
- **Extensie**: Altijd `.md` voor Markdown documenten
- **Beschrijvend**: Naam moet inhoud duidelijk maken
- **Datums**: Gebruik `YYYY-MM-DD` format vooraan indien chronologisch

**Voorbeelden**:
- ✅ `deployment-procedure.md`
- ✅ `2026-01-10-release-notes.md`
- ✅ `api-design-guidelines.md`
- ❌ `Deployment Procedure.md` (spatie, hoofdletter)
- ❌ `doc1.md` (niet beschrijvend)
- ❌ `API_Design.md` (underscore)

---

## Markdown Standaarden

### Document Structuur
Elk Markdown document heeft:

1. **Title** (H1, één keer):
   ```markdown
   # Document Titel
   ```

2. **Metadata** (optioneel, bovenaan):
   ```markdown
   ---
   versie: 1.0
   datum: 2026-01-10
   auteur: Naam
   status: Draft|Review|Approved
   ---
   ```

3. **Hoofdsecties** (H2):
   ```markdown
   ## Sectie Naam
   ```

4. **Subsecties** (H3, H4):
   - Maximaal 4 heading niveaus
   - Logische hiërarchie

### Formatting Conventies
- **Bold** voor belangrijke termen bij eerste gebruik
- *Italic* voor nadruk
- `code` voor technische termen, commando's, bestandsnamen
- > Blockquotes voor citaten en belangrijke opmerkingen

### Links
- **Interne links**: Relatieve paths
  ```markdown
  [zie procedure](../procedures/deployment.md)
  ```
- **Externe links**: Volledige URL's
  ```markdown
  [GitHub Docs](https://docs.github.com)
  ```

### Lijsten
- **Unordered**: Gebruik `-` (niet `*` of `+`)
- **Ordered**: Gebruik `1.`, `2.`, etc.
- **Genest**: Max 2 niveaus, gebruik 2 spaties indent

---

## Validatie Checklist

Gebruik deze checklist bij nieuwe workspace of review:

### Structuur
- [ ] Alle verplichte root folders aanwezig (`/docs`, `/governance`, `/templates`, `/.github`)
- [ ] `/scripts` folder aanwezig indien agents in gebruik
- [ ] Geen folders buiten standaard zonder documentatie waarom
- [ ] Maximaal 3 niveaus diep in folder structuur
- [ ] Geen lege folders in de repository

### Bestanden
- [ ] `README.md` aanwezig met alle verplichte secties
- [ ] `.gitignore` aanwezig met basis uitsluitingen
- [ ] `governance/beleid.md` aanwezig met scope en niet-in-scope
- [ ] Alle documenten in Markdown format

### Naamgeving
- [ ] Alle folder namen lowercase
- [ ] Alle bestandsnamen lowercase met hyphens
- [ ] Geen spaties in folder of bestandsnamen
- [ ] Beschrijvende namen die inhoud duidelijk maken

### Markdown Kwaliteit
- [ ] Elk document heeft één H1 titel
- [ ] Logische heading hiërarchie (H1 → H2 → H3)
- [ ] Interne links gebruiken relatieve paths
- [ ] Consistente lijst formatting (gebruik `-`)
- [ ] Code blocks hebben taal specificatie

### Governance
- [ ] `beleid.md` conform Artikel 9 van Constitutie
- [ ] Geen conflicten met centrale gedragscode
- [ ] Rolbeschrijvingen aanwezig voor actieve agents (indien van toepassing)

---

## Implementatie

### Voor Nieuwe Workspace
1. Creëer basis folderstructuur
2. Kopieer templates uit Genesis
3. Maak `README.md` op basis van template
4. Schrijf `governance/beleid.md` met scope
5. Configureer `.gitignore`
6. Valideer tegen checklist

### Voor Bestaande Workspace
1. Analyseer huidige structuur
2. Map bestaande content naar standaard folders
3. Hernoem folders/bestanden volgens conventies
4. Update alle interne links
5. Voeg ontbrekende verplichte elementen toe
6. Valideer tegen checklist

---

## Uitzonderingen

Uitzonderingen op deze standaard zijn toegestaan wanneer:
- Er een gedocumenteerde reden is in `README.md`
- De uitzondering geen conflicten veroorzaakt met navigatie
- De uitzondering is goedgekeurd door workspace owner

**Documenteer uitzonderingen**:
```markdown
## Structuur Uitzonderingen

### `/custom-folder`
**Reden**: [waarom nodig]
**Goedgekeurd**: [door wie, wanneer]
```

---

## Versiebeheer

- **Versie 1.0** (2026-01-10): Initiële standaard
- Wijzigingen worden gedocumenteerd in dit bestand
- Grote wijzigingen krijgen nieuw versienummer

---

## Referenties

- [Constitutie Artikel 9](gedragscode.md#artikel-9) - Minimale vereisten voor beleid
- [Logos Rolbeschrijving](rolbeschrijvingen/logos.md) - Git/GitHub expert
- [Markdown Guide](https://www.markdownguide.org/) - Markdown best practices

---

**Maintained by**: Logos (Git & GitHub Expert)  
**Status**: Bindend voor alle document-repositories
