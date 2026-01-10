#!/usr/bin/env python3
"""
Runner voor Tennis Trainer agent

Zie: governance/rolbeschrijvingen/tennis-trainer.md
Prompt: .github/prompts/tennis-trainer.prompt.md

Gebruik:
    python scripts/tennis-trainer.py [argumenten]
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Tennis Trainer agent runner",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # TODO: Voeg argumenten toe
    parser.add_argument("opdracht", help="Opdracht voor agent")
    parser.add_argument("--check-only", action="store_true",
                       help="Alleen analyseren, geen wijzigingen")
    
    args = parser.parse_args()
    
    # TODO: Implementeer agent logica
    print(f"{agent_title} agent gestart...")
    print(f"Opdracht: {args.opdracht}")
    
    if args.check_only:
        print("Mode: Alleen analyse (geen wijzigingen)")
    
    # TODO: Voer agent taken uit
    
    print("✅ Klaar")
    return 0


if __name__ == "__main__":
    sys.exit(main())
