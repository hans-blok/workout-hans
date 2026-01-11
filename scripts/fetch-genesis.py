#!/usr/bin/env python3
"""
Genesis Sync Script

Synchroniseert governance documenten, agents en scripts van Genesis naar deze workspace.
Gebruikt wanneer Genesis is geüpdatet en wijzigingen moeten worden overgenomen.

Gebruik:
    python scripts/fetch-genesis.py
    python scripts/fetch-genesis.py --dry-run
    python scripts/fetch-genesis.py --genesis-path "../genesis"
    python scripts/fetch-genesis.py --components governance,agents
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import hashlib


def print_header(text):
    """Print een header met emoji en lijnen"""
    print(f"\n🔄 {text}")
    print("━" * 60)


def print_step(text):
    """Print een stap met checkmark"""
    print(f"✅ {text}")


def print_update(text):
    """Print een update actie"""
    print(f"📝 {text}")


def print_skip(text):
    """Print een skip actie"""
    print(f"⏭️  {text}")


def print_error(text):
    """Print een error met cross"""
    print(f"❌ ERROR: {text}", file=sys.stderr)


def print_warning(text):
    """Print een waarschuwing"""
    print(f"⚠️  WAARSCHUWING: {text}")


def print_info(text):
    """Print info"""
    print(f"ℹ️  {text}")


def find_workspace_root():
    """Vind workspace root (waar governance/ folder staat)"""
    current = Path.cwd()
    
    for parent in [current] + list(current.parents):
        if (parent / "governance").exists():
            return parent
    
    return None


def find_genesis_root(provided_path=None):
    """Vind Genesis repository"""
    if provided_path:
        genesis_path = Path(provided_path)
        if genesis_path.exists() and (genesis_path / "governance/gedragscode.md").exists():
            return genesis_path
    
    # Zoek in parent directories
    workspace_root = find_workspace_root()
    if workspace_root:
        # Probeer sibling directory
        parent = workspace_root.parent
        genesis = parent / "genesis"
        if genesis.exists() and (genesis / "governance/gedragscode.md").exists():
            return genesis
    
    # Probeer environment variable
    import os
    genesis_env = os.environ.get("GENESIS_PATH")
    if genesis_env:
        genesis_path = Path(genesis_env)
        if genesis_path.exists() and (genesis_path / "governance/gedragscode.md").exists():
            return genesis_path
    
    return None


def file_hash(filepath):
    """Bereken MD5 hash van bestand"""
    if not filepath.exists():
        return None
    
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()


def files_identical(file1, file2):
    """Check of twee bestanden identiek zijn"""
    if not file1.exists() or not file2.exists():
        return False
    return file_hash(file1) == file_hash(file2)


def extract_workspace_name(beleid_path):
    """Extract workspace naam uit beleid.md"""
    if not beleid_path.exists():
        return None
    
    content = beleid_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    
    for line in lines:
        if line.startswith("# Beleid:"):
            # Extract naam tussen "# Beleid: " en " Workspace"
            title = line.replace("# Beleid:", "").strip()
            if " Workspace" in title:
                return title.replace(" Workspace", "").strip().lower()
            return title.strip().lower()
    
    return None


def sync_governance(genesis_root, workspace_root, dry_run):
    """Sync governance documenten"""
    print_header("Governance Documenten")
    
    governance_files = [
        "governance/gedragscode.md",
        "governance/workspace-standaard.md",
        "governance/agent-standaard.md"
    ]
    
    updated = []
    skipped = []
    
    for rel_path in governance_files:
        src = genesis_root / rel_path
        dst = workspace_root / rel_path
        
        if not src.exists():
            print_warning(f"Bestand niet gevonden in Genesis: {rel_path}")
            continue
        
        # Check of identiek
        if files_identical(src, dst):
            print_skip(f"{rel_path} (geen wijzigingen)")
            skipped.append(rel_path)
            continue
        
        # Update nodig
        if dry_run:
            print_update(f"{rel_path} (zou worden geüpdatet)")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print_update(f"{rel_path}")
        
        updated.append(rel_path)
    
    return updated, skipped


def sync_agents(genesis_root, workspace_root, workspace_name, dry_run):
    """Sync agent componenten (alle agents uit Genesis behalve Logos)"""
    print_header("Agent Componenten")
    
    # Detecteer alle agents in Genesis
    genesis_agents_dir = genesis_root / "governance/rolbeschrijvingen"
    agents = []
    
    if genesis_agents_dir.exists():
        for rolbeschrijving in genesis_agents_dir.glob("*.md"):
            agent_name = rolbeschrijving.stem
            # Skip Logos en niet-agent bestanden
            if agent_name not in ["logos", "README", "template"]:
                agents.append(agent_name)
        
        print_info(f"Gevonden agents in Genesis: {', '.join(agents)}")
    else:
        print_warning("Geen agents directory gevonden in Genesis")
        return [], []
    
    updated = []
    skipped = []
    
    for agent in agents:
        # Rolbeschrijving
        rolbeschrijving_src = genesis_root / f"governance/rolbeschrijvingen/{agent}.md"
        rolbeschrijving_dst = workspace_root / f"governance/rolbeschrijvingen/{agent}.md"
        
        if rolbeschrijving_src.exists():
            # Lees en vervang workspace naam
            content = rolbeschrijving_src.read_text(encoding="utf-8")
            content = content.replace(f"genesis.{agent}", f"{workspace_name}.{agent}")
            
            # Check of update nodig
            current_content = rolbeschrijving_dst.read_text(encoding="utf-8") if rolbeschrijving_dst.exists() else ""
            
            if content == current_content:
                print_skip(f"{agent} rolbeschrijving (geen wijzigingen)")
                skipped.append(f"{agent}-rolbeschrijving")
            else:
                if dry_run:
                    print_update(f"{agent} rolbeschrijving (zou worden geüpdatet)")
                else:
                    rolbeschrijving_dst.parent.mkdir(parents=True, exist_ok=True)
                    rolbeschrijving_dst.write_text(content, encoding="utf-8")
                    print_update(f"{agent} rolbeschrijving")
                
                updated.append(f"{agent}-rolbeschrijving")
        
        # Prompt
        prompt_src = genesis_root / f".github/prompts/{agent}.prompt.md"
        prompt_dst = workspace_root / f".github/prompts/{agent}.prompt.md"
        
        if prompt_src.exists():
            content = prompt_src.read_text(encoding="utf-8")
            content = content.replace(f"genesis.{agent}", f"{workspace_name}.{agent}")
            
            current_content = prompt_dst.read_text(encoding="utf-8") if prompt_dst.exists() else ""
            
            if content == current_content:
                print_skip(f"{agent} prompt (geen wijzigingen)")
                skipped.append(f"{agent}-prompt")
            else:
                if dry_run:
                    print_update(f"{agent} prompt (zou worden geüpdatet)")
                else:
                    prompt_dst.parent.mkdir(parents=True, exist_ok=True)
                    prompt_dst.write_text(content, encoding="utf-8")
                    print_update(f"{agent} prompt")
                
                updated.append(f"{agent}-prompt")
        
        # Runner (optioneel, kan niet bestaan)
        runner_src = genesis_root / f"scripts/{agent}.py"
        runner_dst = workspace_root / f"scripts/{agent}.py"
        
        if runner_src.exists():
            if files_identical(runner_src, runner_dst):
                print_skip(f"{agent} runner (geen wijzigingen)")
                skipped.append(f"{agent}-runner")
            else:
                if dry_run:
                    print_update(f"{agent} runner (zou worden geüpdatet)")
                else:
                    runner_dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(runner_src, runner_dst)
                    print_update(f"{agent} runner")
                
                updated.append(f"{agent}-runner")
    
    return updated, skipped


def sync_scripts(genesis_root, workspace_root, dry_run):
    """Sync utility scripts"""
    print_header("Utility Scripts")
    
    scripts = [
        "scripts/create-agent.py",
        "scripts/fetch-genesis.py"  # Dit script zelf
    ]
    
    updated = []
    skipped = []
    
    for rel_path in scripts:
        src = genesis_root / rel_path
        dst = workspace_root / rel_path
        
        if not src.exists():
            continue
        
        if files_identical(src, dst):
            print_skip(f"{rel_path} (geen wijzigingen)")
            skipped.append(rel_path)
            continue
        
        if dry_run:
            print_update(f"{rel_path} (zou worden geüpdatet)")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print_update(f"{rel_path}")
        
        updated.append(rel_path)
    
    return updated, skipped


def print_summary(all_updates, all_skips, dry_run):
    """Print samenvatting van sync"""
    print()
    print("━" * 60)
    if dry_run:
        print("🔍 Dry Run Samenvatting")
    else:
        print("✅ Sync Compleet")
    print("━" * 60)
    print()
    
    if all_updates:
        print(f"📝 Geüpdatet: {len(all_updates)} bestand(en)")
        for item in all_updates:
            print(f"   - {item}")
    else:
        print("📝 Geen updates nodig")
    
    if all_skips:
        print(f"\n⏭️  Ongewijzigd: {len(all_skips)} bestand(en)")
    
    if dry_run:
        print("\n💡 Run zonder --dry-run om wijzigingen door te voeren")


def main():
    parser = argparse.ArgumentParser(
        description="Synchroniseer Genesis updates naar deze workspace",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Voorbeelden:
  python scripts/fetch-genesis.py
  python scripts/fetch-genesis.py --dry-run
  python scripts/fetch-genesis.py --genesis-path "../genesis"
  python scripts/fetch-genesis.py --components governance,agents

Componenten:
  governance  - Governance documenten (gedragscode, workspace-standaard, agent-standaard)
  agents      - Agent componenten (alle agents behalve Logos: moeder, rolbeschrijver, publisher, etc.)
  scripts     - Utility scripts (create-agent.py, fetch-genesis.py)
  all         - Alles (default)

Let op: Script doet automatisch een git pull in Genesis repository voor laatste versie
        """
    )
    
    parser.add_argument("--genesis-path",
                       help="Pad naar Genesis repository (auto-detect indien niet gegeven)")
    parser.add_argument("--components", default="all",
                       help="Componenten om te syncen: governance,agents,scripts of all")
    parser.add_argument("--dry-run", action="store_true",
                       help="Preview wijzigingen zonder daadwerkelijk te updaten")
    parser.add_argument("--no-pull", action="store_true",
                       help="Skip git pull in Genesis repository")
    
    args = parser.parse_args()
    
    # Vind workspace root
    workspace_root = find_workspace_root()
    if not workspace_root:
        print_error("Workspace root niet gevonden (geen governance/ folder)")
        print_info("Run dit script vanuit een workspace")
        return 1
    
    # Vind Genesis
    genesis_root = find_genesis_root(args.genesis_path)
    if not genesis_root:
        print_error("Genesis repository niet gevonden")
        print()
        print("Oplossingen:")
        print("1. Geef path op: --genesis-path \"../genesis\"")
        print("2. Plaats Genesis als sibling directory van deze workspace")
        print("3. Set environment variable: GENESIS_PATH=/pad/naar/genesis")
        print()
        return 1
    
    # Git pull in Genesis (tenzij --no-pull)
    if not args.no_pull and not args.dry_run:
        print_header("Genesis Update")
        try:
            result = subprocess.run(["git", "pull"], cwd=genesis_root, 
                                  capture_output=True, text=True, check=True)
            if "Already up to date" in result.stdout:
                print_info("Genesis is al up-to-date")
            else:
                print_step("Genesis geüpdatet via git pull")
                if result.stdout.strip():
                    print(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            print_warning(f"Git pull gefaald: {e}")
            print_info("Ga door met huidige Genesis versie")
    elif args.no_pull:
        print_info("Git pull overgeslagen (--no-pull)")
    
    # Extract workspace naam uit beleid.md
    beleid_path = workspace_root / "governance/beleid.md"
    workspace_name = extract_workspace_name(beleid_path)
    if not workspace_name:
        print_warning("Workspace naam niet gevonden in beleid.md, gebruik 'workspace'")
        workspace_name = "workspace"
    
    # Parse components
    components = args.components.lower().split(",")
    if "all" in components:
        components = ["governance", "agents", "scripts"]
    
    # Header
    print_header("Genesis Sync")
    print(f"Workspace: {workspace_root.name}")
    print(f"Genesis:   {genesis_root}")
    print(f"Mode:      {'Dry Run' if args.dry_run else 'Live Update'}")
    print(f"Components: {', '.join(components)}")
    
    all_updates = []
    all_skips = []
    
    # Sync componenten
    if "governance" in components:
        updated, skipped = sync_governance(genesis_root, workspace_root, args.dry_run)
        all_updates.extend(updated)
        all_skips.extend(skipped)
    
    if "agents" in components:
        updated, skipped = sync_agents(genesis_root, workspace_root, workspace_name, args.dry_run)
        all_updates.extend(updated)
        all_skips.extend(skipped)
    
    if "scripts" in components:
        updated, skipped = sync_scripts(genesis_root, workspace_root, args.dry_run)
        all_updates.extend(updated)
        all_skips.extend(skipped)
    
    # Samenvatting
    print_summary(all_updates, all_skips, args.dry_run)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
