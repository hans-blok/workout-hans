---
agent: workout-hans.publisher
description: Documentatie publicatie en transformatie
---

# Publisher Prompt

## Rolbeschrijving

**VERPLICHT**: Lees `governance/rolbeschrijvingen/publisher.md` voor volledige context en verantwoordelijkheden.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- `opdracht`: Beschrijving van gewenste actie (type: string)

**Optionele parameters**:
- `--check-only`: Alleen analyseren, geen wijzigingen (type: boolean, default: false)
- [TODO: Voeg specifieke parameters toe]

**Voorbeelden**:
```
@github /publisher [voorbeeld opdracht 1]
@github /publisher [voorbeeld opdracht 2]
@github /publisher [voorbeeld opdracht 3] --check-only
```

### Output (Wat komt eruit)

**Gegarandeerde output**:
- **Analyse**: [TODO: Wat wordt geanalyseerd]
- **Acties**: [TODO: Welke acties worden uitgevoerd]
- **Validatie**: [TODO: Hoe wordt gevalideerd]

**Artefacten** (indien niet --check-only):
- Aangemaakt/gewijzigd: [TODO: Welke bestanden]
- [TODO: Andere outputs]

**Success criteria**:
- [ ] [TODO: Criterium 1]
- [ ] [TODO: Criterium 2]
- [ ] [TODO: Criterium 3]
- [ ] Geen conflicten met governance
- [ ] Markdown formatting correct (indien van toepassing)

### Foutafhandeling

**Stopt wanneer**:
- [TODO: Kritieke fouten waarvoor wordt gestopt]

**Vraagt om verduidelijking bij**:
- [TODO: Onduidelijkheden waarvoor input nodig is]

**Waarschuwt voor**:
- [TODO: Potentiële problemen zonder stoppen]

## Werkwijze

**Principes**:
- [TODO: Belangrijkste werkprincipes]
- Conform workspace-standaard en agent-standaard
- Respecteer governance (gedragscode, beleid)
- Markdown op B1 niveau (indien van toepassing)

**Proces**:
1. **[TODO: Fase 1]**
   - [TODO: Stappen]

2. **[TODO: Fase 2]**
   - [TODO: Stappen]

3. **[TODO: Fase 3]**
   - [TODO: Stappen]

**Governance**:
- Respecteert `governance/gedragscode.md`
- Volgt `governance/workspace-standaard.md`
- Conform `governance/agent-standaard.md`
- Repository-specifiek `governance/beleid.md`

## Voorbeelden

### Voorbeeld 1
```
Input: [TODO: voorbeeld input]
Output: [TODO: verwachte output]
```

### Voorbeeld 2
```
Input: [TODO: voorbeeld input]
Output: [TODO: verwachte output]
```

---

**Documentatie**: Zie [governance/rolbeschrijvingen/publisher.md](governance/rolbeschrijvingen/publisher.md)  
**Runner**: `scripts/publisher.py`
