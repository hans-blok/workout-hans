# Workout-hans

Document repository workspace: workout-hans

## Structuur

```
workout-hans/
├── docs/                    # Documentatie
├── governance/              # Governance documenten
│   ├── gedragscode.md
│   ├── workspace-standaard.md
│   ├── agent-standaard.md
│   ├── beleid.md           # Workspace-specifiek beleid
│   └── rolbeschrijvingen/  # Agent rolbeschrijvingen
├── templates/               # Templates
├── scripts/                 # Scripts en runners
├── .github/
│   └── prompts/            # Agent prompts
└── temp/                    # Tijdelijke context (niet in git)
```

## Agents

### Moeder (workout-hans.moeder)
Git en GitHub expert + workspace ordening

**Gebruik**:
```
@github /moeder Richt workspace in volgens standaard
@github /moeder Valideer markdown formatting
```

### Rolbeschrijver (workout-hans.rolbeschrijver)
Specialist in agent documentatie

**Gebruik**:
```
@github /rolbeschrijver agent-naam=mijn-agent doel="..." domein="..."
```

## Nieuwe Agent Toevoegen

```bash
# 1. Maak rolbeschrijving met rolbeschrijver agent
@github /rolbeschrijver agent-naam=mijn-agent doel="Korte omschrijving" domein="kennisgebied"

# 2. Genereer agent skeletons (prompt + runner)
python scripts/create-agent.py mijn-agent

# 3. Vul prompt contract in
# Edit: .github/prompts/mijn-agent.prompt.md

# 4. Test agent
@github /mijn-agent [opdracht]
```

## Governance

Deze workspace volgt de governance standaarden uit Genesis:
- **Gedragscode**: B1 Nederlands, fatsoenlijk, testbaar
- **Workspace-standaard**: Folders, naamgeving, markdown
- **Agent-standaard**: 3 componenten (rolbeschrijving, prompt, runner)

Zie `governance/beleid.md` voor workspace-specifiek beleid en scope.

---

**Versie**: 1.0  
**Aangemaakt**: 10 January 2026  
**Geïnitialiseerd met**: Genesis init-workspace.py
