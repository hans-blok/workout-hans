#!/usr/bin/env python3
"""
Agent Skeleton Generator

Genereert prompt en runner skeletons voor een nieuwe agent.
VEREIST: Rolbeschrijving moet al bestaan in governance/rolbeschrijvingen/

Gebruik:
    python scripts/create-agent.py agent-naam
    python scripts/create-agent.py validator
    python scripts/create-agent.py recept-schrijver
"""

import argparse
import sys
from pathlib import Path
from datetime import date


def print_error(text):
    """Print een error met cross"""
    print(f"❌ ERROR: {text}", file=sys.stderr)


def print_success(text):
    """Print success met checkmark"""
    print(f"✅ {text}")


def print_info(text):
    """Print info"""
    print(f"ℹ️  {text}")


def validate_agent_name(agent_name):
    """Valideer agent naam volgens conventies"""
    if not agent_name:
        return False, "Agent naam mag niet leeg zijn"
    
    if not agent_name.islower():
        return False, "Agent naam moet lowercase zijn"
    
    if " " in agent_name:
        return False, "Gebruik hyphens i.p.v. spaties"
    
    if not all(c.isalnum() or c == "-" for c in agent_name):
        return False, "Alleen letters, cijfers en hyphens toegestaan"
    
    return True, ""


def find_workspace_root():
    """Vind workspace root (waar governance/ folder staat)"""
    current = Path.cwd()
    
    # Zoek naar governance folder
    for parent in [current] + list(current.parents):
        if (parent / "governance").exists():
            return parent
    
    return None


def extract_metadata(rolbeschrijving_content):
    """Extract metadata uit rolbeschrijving"""
    lines = rolbeschrijving_content.split("\n")
    metadata = {}
    
    for line in lines:
        if line.startswith("**Agent**:"):
            metadata["agent"] = line.split(":", 1)[1].strip()
        elif line.startswith("**Domein**:"):
            metadata["domein"] = line.split(":", 1)[1].strip()
        elif line.startswith("**Type**:"):
            metadata["type"] = line.split(":", 1)[1].strip()
        elif line.startswith("# Rolbeschrijving:"):
            metadata["title"] = line.replace("# Rolbeschrijving:", "").strip()
        
        # Stop na eerste hoofdsectie
        if line.startswith("## ") and metadata:
            break
    
    return metadata


def generate_prompt_skeleton(agent_name, metadata, workspace_name):
    """Genereer prompt skeleton"""
    
    agent_title = metadata.get("title", agent_name.capitalize())
    agent_id = metadata.get("agent", f"{workspace_name}.{agent_name}")
    domein = metadata.get("domein", "TODO: specificeer domein")
    
    prompt = f"""---
agent: {agent_id}
description: {domein}
---

# {agent_title} Prompt

## Rolbeschrijving

**VERPLICHT**: Lees `governance/rolbeschrijvingen/{agent_name}.md` voor volledige context en verantwoordelijkheden.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- `opdracht`: Beschrijving van gewenste actie (type: string)

**Optionele parameters**:
- `--check-only`: Alleen analyseren, geen wijzigingen (type: boolean, default: false)
- [TODO: Voeg specifieke parameters toe]

**Voorbeelden**:
```
@github /{agent_name} [voorbeeld opdracht 1]
@github /{agent_name} [voorbeeld opdracht 2]
@github /{agent_name} [voorbeeld opdracht 3] --check-only
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

**Documentatie**: Zie [governance/rolbeschrijvingen/{agent_name}.md](governance/rolbeschrijvingen/{agent_name}.md)  
**Runner**: `scripts/{agent_name}.py`
"""
    
    return prompt


def generate_runner_skeleton(agent_name, metadata):
    """Genereer Python runner skeleton"""
    
    agent_title = metadata.get("title", agent_name.capitalize())
    
    runner = f"""#!/usr/bin/env python3
\"\"\"
Runner voor {agent_title} agent

Zie: governance/rolbeschrijvingen/{agent_name}.md
Prompt: .github/prompts/{agent_name}.prompt.md

Gebruik:
    python scripts/{agent_name}.py [argumenten]
\"\"\"

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="{agent_title} agent runner",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # TODO: Voeg argumenten toe
    parser.add_argument("opdracht", help="Opdracht voor agent")
    parser.add_argument("--check-only", action="store_true",
                       help="Alleen analyseren, geen wijzigingen")
    
    args = parser.parse_args()
    
    # TODO: Implementeer agent logica
    print(f"{{agent_title}} agent gestart...")
    print(f"Opdracht: {{args.opdracht}}")
    
    if args.check_only:
        print("Mode: Alleen analyse (geen wijzigingen)")
    
    # TODO: Voer agent taken uit
    
    print("✅ Klaar")
    return 0


if __name__ == "__main__":
    sys.exit(main())
"""
    
    return runner


def main():
    parser = argparse.ArgumentParser(
        description="Genereer agent skeletons (prompt + runner) voor bestaande rolbeschrijving",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Voorbeelden:
  python scripts/create-agent.py validator
  python scripts/create-agent.py recept-schrijver

BELANGRIJK: Rolbeschrijving moet al bestaan in governance/rolbeschrijvingen/
Maak eerst een rolbeschrijving met: @github /rolbeschrijver
        """
    )
    
    parser.add_argument("agent_name", 
                       help="Agent naam (moet matchen met rolbeschrijving)")
    
    args = parser.parse_args()
    agent_name = args.agent_name
    
    # Valideer agent naam
    valid, error_msg = validate_agent_name(agent_name)
    if not valid:
        print_error(f"Ongeldige agent naam: {error_msg}")
        return 1
    
    # Vind workspace root
    workspace_root = find_workspace_root()
    if not workspace_root:
        print_error("Workspace root niet gevonden (geen governance/ folder)")
        print_info("Run dit script vanuit een workspace met governance structuur")
        return 1
    
    # Controleer of rolbeschrijving bestaat
    rolbeschrijving_path = workspace_root / f"governance/rolbeschrijvingen/{agent_name}.md"
    
    if not rolbeschrijving_path.exists():
        print_error("Rolbeschrijving niet gevonden")
        print()
        print(f"   Verwacht: {rolbeschrijving_path}")
        print()
        print("   Maak eerst een rolbeschrijving:")
        print(f"   @github /rolbeschrijver agent-naam={agent_name} doel=\"...\" domein=\"...\"")
        print()
        return 1
    
    # Lees rolbeschrijving
    rolbeschrijving_content = rolbeschrijving_path.read_text(encoding="utf-8")
    metadata = extract_metadata(rolbeschrijving_content)
    
    # Bepaal workspace naam uit agent identifier of gebruik generic
    workspace_name = "workspace"
    if "agent" in metadata and "." in metadata["agent"]:
        workspace_name = metadata["agent"].split(".")[0]
    
    # Genereer prompt skeleton
    prompt_path = workspace_root / f".github/prompts/{agent_name}.prompt.md"
    
    if prompt_path.exists():
        print_error(f"Prompt bestaat al: {prompt_path}")
        print_info("Verwijder eerst het bestaande bestand of gebruik een andere naam")
        return 1
    
    prompt_content = generate_prompt_skeleton(agent_name, metadata, workspace_name)
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(prompt_content, encoding="utf-8")
    print_success(f"Prompt skeleton aangemaakt: {prompt_path}")
    
    # Genereer runner skeleton
    runner_path = workspace_root / f"scripts/{agent_name}.py"
    
    if runner_path.exists():
        print_error(f"Runner bestaat al: {runner_path}")
        print_info("Verwijder eerst het bestaande bestand of gebruik een andere naam")
        return 1
    
    runner_content = generate_runner_skeleton(agent_name, metadata)
    runner_path.parent.mkdir(parents=True, exist_ok=True)
    runner_path.write_text(runner_content, encoding="utf-8")
    print_success(f"Runner skeleton aangemaakt: {runner_path}")
    
    # Success bericht
    print()
    print("━" * 60)
    print(f"✅ Agent skeletons aangemaakt voor '{agent_name}'")
    print("━" * 60)
    print()
    print("Volgende stappen:")
    print(f"1. Vul prompt contract in: .github/prompts/{agent_name}.prompt.md")
    print(f"2. Implementeer runner: scripts/{agent_name}.py")
    print(f"3. Test agent: @github /{agent_name} [opdracht]")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
