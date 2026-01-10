#!/usr/bin/env python3
"""
Runner voor Publisher agent

Converteert Markdown documenten naar PDF en HTML met Pandoc.

Zie: governance/rolbeschrijvingen/publisher.md
Prompt: .github/prompts/publisher.prompt.md

Gebruik:
    python scripts/publisher.py document.md
    python scripts/publisher.py document.md --format pdf
    python scripts/publisher.py docs/*.md --output-dir build
    python scripts/publisher.py document.md --check-only
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def print_header(text):
    """Print een header met emoji"""
    print(f"\n📄 {text}")
    print("━" * 60)


def print_step(text):
    """Print een stap met checkmark"""
    print(f"✓ {text}")


def print_error(text):
    """Print een error met emoji"""
    print(f"❌ ERROR: {text}")


def print_warning(text):
    """Print een warning met emoji"""
    print(f"⚠️  WAARSCHUWING: {text}")


def print_info(text):
    """Print info met emoji"""
    print(f"ℹ️  {text}")


def check_pandoc():
    """Check of Pandoc geïnstalleerd is"""
    if not shutil.which("pandoc"):
        print_error("Pandoc niet gevonden")
        print()
        print("Installatie:")
        print("  Windows:  winget install pandoc")
        print("            choco install pandoc")
        print("  Mac:      brew install pandoc")
        print("  Linux:    apt install pandoc  (Ubuntu/Debian)")
        print()
        return False
    return True


def get_pandoc_version():
    """Haal Pandoc versie op"""
    try:
        result = subprocess.run(["pandoc", "--version"], 
                              capture_output=True, text=True, check=True)
        first_line = result.stdout.split('\n')[0]
        return first_line.replace("pandoc ", "")
    except subprocess.CalledProcessError:
        return "onbekend"


def convert_to_pdf(input_file, output_file, metadata=None):
    """Converteer MD naar PDF met Pandoc"""
    cmd = [
        "pandoc",
        str(input_file),
        "-o", str(output_file),
        "--pdf-engine=xelatex",  # Betere Unicode support
        "-V", "geometry:margin=2.5cm",
        "--toc",  # Table of contents
        "--toc-depth=3"
    ]
    
    # Metadata toevoegen
    if metadata:
        if metadata.get("title"):
            cmd.extend(["-M", f"title={metadata['title']}"])
        if metadata.get("author"):
            cmd.extend(["-M", f"author={metadata['author']}"])
        if metadata.get("date"):
            cmd.extend(["-M", f"date={metadata['date']}"])
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True, None
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def convert_to_html(input_file, output_file, standalone=True):
    """Converteer MD naar HTML met Pandoc"""
    cmd = [
        "pandoc",
        str(input_file),
        "-o", str(output_file),
        "--toc",
        "--toc-depth=3"
    ]
    
    if standalone:
        cmd.append("--standalone")
        cmd.extend(["-c", "https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.0/github-markdown.min.css"])
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True, None
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def check_links(input_file):
    """Check links in Markdown bestand (basis implementatie)"""
    content = input_file.read_text(encoding="utf-8")
    
    # Zoek naar markdown links: [text](url)
    import re
    links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
    
    broken_links = []
    for text, url in links:
        # Check alleen lokale bestanden
        if not url.startswith(('http://', 'https://', '#', 'mailto:')):
            link_path = input_file.parent / url
            if not link_path.exists():
                broken_links.append((text, url))
    
    return broken_links


def process_file(input_file, output_dir, formats, check_only, metadata):
    """Process een enkel bestand"""
    print_info(f"Verwerken: {input_file.name}")
    
    # Check links
    if check_only:
        broken_links = check_links(input_file)
        if broken_links:
            print_warning(f"Gevonden {len(broken_links)} gebroken link(s):")
            for text, url in broken_links:
                print(f"  - [{text}]({url})")
        else:
            print_step("Alle links OK")
        return True
    
    # Converteer naar gewenste formaten
    success = True
    
    if "pdf" in formats:
        output_file = output_dir / f"{input_file.stem}.pdf"
        print_info(f"Genereren: {output_file.name}")
        ok, error = convert_to_pdf(input_file, output_file, metadata)
        if ok:
            print_step(f"PDF: {output_file}")
        else:
            print_error(f"PDF conversie gefaald: {error}")
            success = False
    
    if "html" in formats:
        output_file = output_dir / f"{input_file.stem}.html"
        print_info(f"Genereren: {output_file.name}")
        ok, error = convert_to_html(input_file, output_file)
        if ok:
            print_step(f"HTML: {output_file}")
        else:
            print_error(f"HTML conversie gefaald: {error}")
            success = False
    
    return success


def main():
    parser = argparse.ArgumentParser(
        description="Publisher agent - Converteer Markdown naar PDF/HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Voorbeelden:
  python scripts/publisher.py document.md
  python scripts/publisher.py document.md --format pdf
  python scripts/publisher.py document.md --format html
  python scripts/publisher.py docs/*.md --output-dir build
  python scripts/publisher.py document.md --check-only
  python scripts/publisher.py document.md --title "Mijn Document" --author "Hans"

Output:
  Bestanden worden geplaatst in output directory (default: huidige directory)
  PDF gebruikt xelatex engine met table of contents
  HTML gebruikt GitHub Markdown CSS styling
        """
    )
    
    parser.add_argument("files", nargs="+", help="Markdown bestand(en) om te converteren")
    parser.add_argument("--format", choices=["pdf", "html", "both"], default="both",
                       help="Output formaat (default: both)")
    parser.add_argument("--output-dir", type=Path, default=Path.cwd(),
                       help="Output directory (default: huidige directory)")
    parser.add_argument("--check-only", action="store_true",
                       help="Alleen links checken, geen conversie")
    parser.add_argument("--title", help="Document titel (metadata)")
    parser.add_argument("--author", help="Document auteur (metadata)")
    parser.add_argument("--date", help="Document datum (metadata)")
    
    args = parser.parse_args()
    
    # Check Pandoc
    if not check_pandoc():
        return 1
    
    # Header
    print_header("Publisher Agent")
    pandoc_version = get_pandoc_version()
    print(f"Pandoc versie: {pandoc_version}")
    
    if args.check_only:
        print("Mode: Link check (geen conversie)")
    else:
        formats = ["pdf", "html"] if args.format == "both" else [args.format]
        print(f"Formaten: {', '.join(formats)}")
        print(f"Output: {args.output_dir}")
    
    # Metadata
    metadata = {}
    if args.title:
        metadata["title"] = args.title
    if args.author:
        metadata["author"] = args.author
    if args.date:
        metadata["date"] = args.date
    
    # Output directory maken
    if not args.check_only:
        args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Verwerk bestanden
    print()
    formats = ["pdf", "html"] if args.format == "both" else [args.format]
    
    all_success = True
    processed = 0
    
    for file_pattern in args.files:
        # Glob support
        if "*" in file_pattern or "?" in file_pattern:
            files = list(Path.cwd().glob(file_pattern))
        else:
            files = [Path(file_pattern)]
        
        for input_file in files:
            if not input_file.exists():
                print_error(f"Bestand niet gevonden: {input_file}")
                all_success = False
                continue
            
            if not input_file.suffix == ".md":
                print_warning(f"Overslaan (geen .md): {input_file}")
                continue
            
            success = process_file(input_file, args.output_dir, formats, 
                                 args.check_only, metadata)
            if success:
                processed += 1
            else:
                all_success = False
            
            print()
    
    # Samenvatting
    print("━" * 60)
    if all_success:
        print(f"✅ Klaar: {processed} bestand(en) verwerkt")
    else:
        print(f"⚠️  Compleet met fouten: {processed} bestand(en) verwerkt")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
