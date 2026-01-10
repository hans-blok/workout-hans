#!/usr/bin/env python3
"""
Workspace Initialisatie Script

Maakt een nieuwe document-repository workspace aan met:
- Folderstructuur volgens workspace-standaard
- Governance documenten van Genesis
- Agent moeder en rolbeschrijver
- Beleid.md gegenereerd uit context
- Git repository initialisatie

Gebruik:
    python scripts/init-workspace.py --name "mijn-workspace" --description "Korte omschrijving"
    python scripts/init-workspace.py --name "kerstmenu" --context "temp/kerstmenu-context.md"
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import date


def print_header(text):
    """Print een header met emoji en lijnen"""
    print(f"\n🚀 {text}")
    print("━" * 60)


def print_step(text):
    """Print een stap met checkmark"""
    print(f"✅ {text}")


def print_error(text):
    """Print een error met cross"""
    print(f"❌ ERROR: {text}", file=sys.stderr)


def print_warning(text):
    """Print een waarschuwing"""
    print(f"⚠️  WAARSCHUWING: {text}")


def validate_name(name):
    """Valideer workspace naam volgens conventies"""
    if not name:
        return False, "Naam mag niet leeg zijn"
    
    if not name.islower():
        return False, "Naam moet lowercase zijn"
    
    if " " in name:
        return False, "Gebruik hyphens i.p.v. spaties"
    
    if not all(c.isalnum() or c == "-" for c in name):
        return False, "Alleen letters, cijfers en hyphens toegestaan"
    
    return True, ""


def workspace_exists(name, parent_dir):
    """Controleer of workspace al bestaat"""
    workspace_path = Path(parent_dir) / name
    return workspace_path.exists()


def get_genesis_root():
    """Vind de Genesis root directory"""
    script_dir = Path(__file__).parent
    genesis_root = script_dir.parent
    
    # Als dit script in Genesis zit, return die
    if (genesis_root / "governance/gedragscode.md").exists():
        return genesis_root
    
    # Zoek in sibling directories (als script gekopieerd is)
    current = Path.cwd()
    parent = current.parent
    genesis = parent / "genesis"
    if genesis.exists() and (genesis / "governance/gedragscode.md").exists():
        return genesis
    
    # Zoek in environment variable
    import os
    genesis_env = os.environ.get("GENESIS_PATH")
    if genesis_env:
        genesis_path = Path(genesis_env)
        if genesis_path.exists() and (genesis_path / "governance/gedragscode.md").exists():
            return genesis_path
    
    return None


def create_folders(workspace_path):
    """Maak folderstructuur aan volgens workspace-standaard"""
    folders = [
        "docs",
        "governance/rolbeschrijvingen",
        "templates",
        "scripts",
        ".github/prompts",
        "temp"
    ]
    
    for folder in folders:
        folder_path = workspace_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
    
    return folders


def copy_governance_documents(genesis_root, workspace_path):
    """Kopieer governance documenten van Genesis"""
    governance_files = [
        "governance/gedragscode.md",
        "governance/workspace-standaard.md",
        "governance/agent-standaard.md"
    ]
    
    for file in governance_files:
        src = genesis_root / file
        dst = workspace_path / file
        
        if src.exists():
            shutil.copy2(src, dst)
        else:
            print_warning(f"Governance bestand niet gevonden: {file}")
    
    return governance_files


def extract_section(content, header):
    """Extract een sectie uit markdown content"""
    lines = content.split("\n")
    in_section = False
    section_lines = []
    
    for line in lines:
        if line.startswith("### ") and header.lower() in line.lower():
            in_section = True
            continue
        elif line.startswith("### ") and in_section:
            break
        elif in_section and line.strip():
            section_lines.append(line)
    
    return "\n".join(section_lines).strip()


def generate_beleid(workspace_name, description, context_content):
    """Genereer beleid.md uit context"""
    
    # Extract secties uit context
    scope_wel = extract_section(context_content, "Wat valt binnen")
    scope_niet = extract_section(context_content, "Wat valt NIET binnen")
    
    # Basis template
    beleid = f"""# Beleid: {workspace_name.capitalize()} Workspace

**Versie**: 1.0  
**Datum**: {date.today().strftime('%d %B %Y')}

---

## Context

{description}

## Scope

### WEL binnen deze workspace

{scope_wel if scope_wel else "- [TODO: Definieer wat binnen scope valt]"}

### NIET binnen deze workspace

{scope_niet if scope_niet else "- [TODO: Definieer wat buiten scope valt]"}

## Agents

### Moeder ({workspace_name}.moeder)
**Rol**: Git/GitHub expert en workspace ordening  
**Verantwoordelijk voor**: Repository structuur, Git workflows, markdown formatting, naamgevingsconventies

**Zie**: `governance/rolbeschrijvingen/moeder.md`

### Rolbeschrijver ({workspace_name}.rolbeschrijver)
**Rol**: Agent documentatie specialist  
**Verantwoordelijk voor**: Rolbeschrijvingen maken voor nieuwe agents volgens agent-standaard

**Zie**: `governance/rolbeschrijvingen/rolbeschrijver.md`

## Kwaliteitsnormen

Conform governance documenten:
- **Gedragscode**: B1 taalniveau, fatsoenlijke omgangsvormen, testbare normen
- **Workspace-standaard**: Folderstructuur, naamgeving, markdown formatting
- **Agent-standaard**: 3-component model (rolbeschrijving, prompt, runner)

### Specifieke normen voor deze workspace

- [ ] Documenten in B1 Nederlands
- [ ] Bestandsnamen lowercase met hyphens
- [ ] Markdown formatting volgens standaard
- [ ] Scope wordt gerespecteerd (WEL/NIET)
- [ ] Nieuwe agents conform agent-standaard

---

**Let op**: Dit beleid is gegenereerd bij workspace initialisatie.  
Pas aan indien scope of agents wijzigen.
"""
    
    return beleid


def copy_agent(agent_name, genesis_root, workspace_path, workspace_name):
    """Kopieer agent componenten en pas aan voor workspace"""
    
    # 1. Rolbeschrijving
    rolbeschrijving_src = genesis_root / f"governance/rolbeschrijvingen/{agent_name}.md"
    rolbeschrijving_dst = workspace_path / f"governance/rolbeschrijvingen/{agent_name}.md"
    
    if rolbeschrijving_src.exists():
        content = rolbeschrijving_src.read_text(encoding="utf-8")
        # Vervang genesis. met workspace.
        content = content.replace(f"genesis.{agent_name}", f"{workspace_name}.{agent_name}")
        rolbeschrijving_dst.write_text(content, encoding="utf-8")
    
    # 2. Prompt
    prompt_src = genesis_root / f".github/prompts/{agent_name}.prompt.md"
    prompt_dst = workspace_path / f".github/prompts/{agent_name}.prompt.md"
    
    if prompt_src.exists():
        content = prompt_src.read_text(encoding="utf-8")
        content = content.replace(f"genesis.{agent_name}", f"{workspace_name}.{agent_name}")
        prompt_dst.write_text(content, encoding="utf-8")
    
    # 3. Runner (optioneel, kan nog niet bestaan)
    runner_src = genesis_root / f"scripts/{agent_name}.py"
    runner_dst = workspace_path / f"scripts/{agent_name}.py"
    
    if runner_src.exists():
        shutil.copy2(runner_src, runner_dst)


def copy_utility_scripts(genesis_root, workspace_path):
    """Kopieer utility scripts naar workspace"""
    scripts = [
        "scripts/create-agent.py",
        "scripts/fetch-genesis.py"
    ]
    
    copied = []
    for script_path in scripts:
        src = genesis_root / script_path
        dst = workspace_path / script_path
        
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied.append(script_path)
        else:
            print_warning(f"{script_path} niet gevonden in Genesis")
    
    return copied


def generate_readme(workspace_name, description, workspace_path):
    """Genereer README.md voor workspace"""
    
    readme = f"""# {workspace_name.capitalize()}

{description}

## Structuur

```
{workspace_name}/
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

### Moeder ({workspace_name}.moeder)
Git en GitHub expert + workspace ordening

**Gebruik**:
```
@github /moeder Richt workspace in volgens standaard
@github /moeder Valideer markdown formatting
```

### Rolbeschrijver ({workspace_name}.rolbeschrijver)
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
**Aangemaakt**: {date.today().strftime('%d %B %Y')}  
**Geïnitialiseerd met**: Genesis init-workspace.py
"""
    
    readme_path = workspace_path / "README.md"
    readme_path.write_text(readme, encoding="utf-8")


def generate_gitignore(workspace_path):
    """Genereer .gitignore voor workspace"""
    
    gitignore = """# Conform workspace-standaard.md

# Tijdelijke context folder
/temp/

# Editor bestanden
.vscode/
.idea/
*.sublime-project
*.sublime-workspace

# OS bestanden
.DS_Store
Thumbs.db
desktop.ini

# Python
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
*.egg-info/
dist/
build/

# Notities en drafts
*.draft.md
*.wip.md
"""
    
    gitignore_path = workspace_path / ".gitignore"
    gitignore_path.write_text(gitignore, encoding="utf-8")


def add_to_git(workspace_path, workspace_name):
    """Voeg workspace toe aan bestaande git repository"""
    try:
        # Check of we in een git repo zitten
        result = subprocess.run(["git", "rev-parse", "--git-dir"], 
                              cwd=workspace_path.parent, 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print_warning("Geen git repository gevonden, overslaan")
            return False
        
        # Git add
        subprocess.run(["git", "add", str(workspace_path)], 
                      cwd=workspace_path.parent, check=True,
                      capture_output=True, text=True)
        
        return True
    except subprocess.CalledProcessError as e:
        print_warning(f"Git add gefaald: {e}")
        return False


def print_success_message(workspace_name, workspace_path, git_added):
    """Print success bericht met volgende stappen"""
    print()
    print("━" * 60)
    print(f"✅ Workspace '{workspace_name}' succesvol aangemaakt!")
    print("━" * 60)
    print()
    print(f"📁 Locatie: {workspace_path}")
    print(f"🔧 Agents: moeder, rolbeschrijver")
    print(f"📄 Beleid: governance/beleid.md")
    if git_added:
        print(f"📝 Git: Bestanden toegevoegd (staged, nog niet gecommit)")
    print()
    print("Volgende stappen:")
    print(f"1. cd {workspace_path.name}")
    print("2. Beschrijf workspace context: edit temp/context.md")
    print("3. Controleer governance/beleid.md (gegenereerd uit context)")
    print("4. Start workspace ordening: @github /moeder Richt workspace in")
    print()
    print("Agents toevoegen:")
    print("1. Doe voorstel in temp/agent-voorstellen.md")
    print("2. Maak rolbeschrijving: @github /rolbeschrijver agent-naam=... doel=\"...\" domein=\"...\"")
    print("3. Genereer agent: python scripts/create-agent.py agent-naam")
    print("4. Vul prompt contract in: .github/prompts/agent-naam.prompt.md")
    print("5. Test agent: @github /agent-naam [opdracht]")
    if git_added:
        print()
        print("Git workflow:")
        print("1. Review wijzigingen: git status")
        print(f"2. Commit: git commit -m \"Initialize {workspace_name} workspace\"")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Initialiseer een nieuwe document-repository workspace",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=r"""
Voorbeelden:
  # In Genesis, maak subdirectory:
  cd c:\gitrepo\genesis
  python scripts/init-workspace.py --name "kerstmenu"
  
  # In lege directory, initialiseer huidige directory:
  cd c:\gitrepo\kerstmenu-2025
  python init-workspace.py
  
  # Met context:
  python init-workspace.py --context "../genesis/temp/context.md"
  
  # Force overschrijven:
  python init-workspace.py --force

Let op:
  - Zonder --name: gebruikt huidige directory naam
  - Als directory naam == workspace naam: initialiseert DEZE directory
  - Anders: maakt subdirectory aan
  - Genesis wordt automatisch gezocht in sibling directories
  - Bestanden worden automatisch toegevoegd aan git (staged) als git repo aanwezig
        """
    )
    
    parser.add_argument("--name",
                       help="Workspace naam (lowercase, hyphens) - default: huidige directory naam")
    parser.add_argument("--description", 
                       help="Korte omschrijving van workspace doel")
    parser.add_argument("--context", 
                       help="Pad naar context.md bestand (voor beleid generatie)")
    parser.add_argument("--force", action="store_true",
                       help="Overschrijf bestaande bestanden zonder te vragen")
    
    args = parser.parse_args()
    
    # Genesis root vinden
    genesis_root = get_genesis_root()
    if not genesis_root:
        print_error("Genesis repository niet gevonden")
        print()
        print("Oplossingen:")
        print("1. Plaats Genesis als sibling directory van deze workspace")
        print("2. Set environment variable: GENESIS_PATH=/pad/naar/genesis")
        print("3. Kopieer dit script naar Genesis en draai daar")
        print()
        return 1
    
    # Huidige directory
    current_dir = Path.cwd()
    
    # Bepaal workspace naam en locatie
    if not args.name:
        # Gebruik huidige directory naam als default
        args.name = current_dir.name
        print("🚀 Nieuwe Workspace Initialisatie")
        print("━" * 60)
        print(f"Gedetecteerde naam: {args.name}")
        
        # Valideer naam
        valid, error_msg = validate_name(args.name)
        if not valid:
            print_warning(f"Directory naam voldoet niet aan conventies: {error_msg}")
            args.name = input("Workspace naam (lowercase, hyphens): ").strip()
            if not args.name:
                print_error("Workspace naam is verplicht")
                return 1
    
    # Validatie
    valid, error_msg = validate_name(args.name)
    if not valid:
        print_error(f"Ongeldige workspace naam: {error_msg}")
        return 1
    
    # Bepaal of we in huidige directory of subdirectory initialiseren
    if current_dir.name == args.name:
        # Initialiseer huidige directory
        workspace_path = current_dir
        
        # Check of directory leeg is (behalve .git en init-workspace.py)
        existing_items = [
            item for item in workspace_path.iterdir()
            if item.name not in ['.git', 'init-workspace.py', '.gitignore', '__pycache__']
        ]
        
        if existing_items and not args.force:
            print_warning(f"Directory is niet leeg: {len(existing_items)} item(s)")
            confirm = input("Doorgaan en overschrijven? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Geannuleerd")
                return 0
        elif existing_items and args.force:
            print_info(f"Directory is niet leeg, maar --force gegeven: {len(existing_items)} item(s) worden overschreven indien nodig")
    else:
        # Maak subdirectory
        workspace_path = current_dir / args.name
        
        # Check of workspace al bestaat
        if workspace_path.exists() and not args.force:
            print_error(f"Workspace '{args.name}' bestaat al in {current_dir}")
            print_info("Gebruik --force om toch door te gaan")
            return 1
        elif workspace_path.exists() and args.force:
            print_info(f"Workspace '{args.name}' bestaat al, maar --force gegeven: bestanden worden overschreven")
    
    # Description
    description = args.description or f"Document repository workspace: {args.name}"
    
    # Context laden (optioneel)
    context_content = None
    if args.context:
        context_path = genesis_root / args.context
        if not context_path.exists():
            print_warning(f"Context bestand niet gevonden: {args.context}")
        else:
            context_content = context_path.read_text(encoding="utf-8")
    
    # Start initialisatie
    print_header(f"Workspace Initialisatie: {args.name}")
    
    # 1. Folders aanmaken
    create_folders(workspace_path)
    print_step("Folderstructuur aangemaakt")
    
    # 2. Governance documenten kopiëren
    copy_governance_documents(genesis_root, workspace_path)
    print_step("Governance documenten gekopieerd")
    
    # 3. Beleid genereren
    if context_content:
        beleid_content = generate_beleid(args.name, description, context_content)
    else:
        # Basis beleid zonder context
        beleid_content = generate_beleid(args.name, description, "")
    
    beleid_path = workspace_path / "governance/beleid.md"
    beleid_path.write_text(beleid_content, encoding="utf-8")
    print_step("Beleid.md gegenereerd")
    
    # 4. Agent moeder installeren
    copy_agent("moeder", genesis_root, workspace_path, args.name)
    print_step("Agent moeder geïnstalleerd")
    
    # 5. Agent rolbeschrijver installeren
    copy_agent("rolbeschrijver", genesis_root, workspace_path, args.name)
    print_step("Agent rolbeschrijver geïnstalleerd")
    
    # 6. Utility scripts kopiëren
    copied_scripts = copy_utility_scripts(genesis_root, workspace_path)
    if copied_scripts:
        print_step(f"Utility scripts gekopieerd: {', '.join([s.split('/')[-1] for s in copied_scripts])}")
    
    # 7. Context template kopiëren naar temp
    context_template_src = genesis_root / "templates/context-template.md"
    context_dst = workspace_path / "temp/context.md"
    
    if context_template_src.exists():
        # Lees template en vul workspace naam in
        template_content = context_template_src.read_text(encoding="utf-8")
        template_content = template_content.replace("[Datum invullen]", date.today().strftime('%d %B %Y'))
        template_content = template_content.replace("[Draft / In Review / Final]", "Draft")
        
        context_dst.write_text(template_content, encoding="utf-8")
        print_step("Context template gekopieerd naar temp/context.md")
    else:
        print_warning("Context template niet gevonden, overslaan")
    
    # 8. README genereren
    generate_readme(args.name, description, workspace_path)
    print_step("README.md gegenereerd")
    
    # 9. .gitignore genereren
    generate_gitignore(workspace_path)
    print_step(".gitignore aangemaakt")
    
    # 10. Toevoegen aan git (indien aanwezig)
    git_added = add_to_git(workspace_path, args.name)
    if git_added:
        print_step("Bestanden toegevoegd aan git (staged, temp/ uitgesloten)")
    
    # Success!
    print_success_message(args.name, workspace_path, git_added)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
