#!/usr/bin/env python3
"""validate_facts.py — Cross-validation entre referencias canonicas + drafts.

Modo 1 (--refs): valida que as referencias da skill nao tenham fatos divergentes
entre si (caso real de invasao: equipe.md tinha "Rayssa Pereira Mendes do Nascimento"
45% enquanto empresa-manaca.md tinha "Rayssa Pereira do Nascimento Mendes" 65%).

Modo 2 (--draft <path>): valida que um draft de proposta (markdown) nao contenha
fatos divergentes do canonico em empresa-manaca.md.

Uso:
    python validate_facts.py --refs
    python validate_facts.py --draft c:/Editais/editais/<slug>/05a-data-pack.md
    python validate_facts.py --refs --draft <path>   # ambos os modos

Exit code 0 se OK; 1 se houver divergencia.

Dependencias: nenhuma alem de stdlib (parse YAML manual, regex em vez de PyYAML).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REFERENCES_DIR = Path(__file__).resolve().parent.parent / "references"

# Fatos canonicos esperados em empresa-manaca.md (fonte de verdade).
# Cada entry tem (label, regex_pattern_para_extrair, valor_esperado).
# A regex deve casar contra o conteudo do markdown.
CANONICAL_FACTS = {
    "cnpj_manaca": {
        "label": "CNPJ Manaca",
        "regex": r"48\.612\.137/0001-23",
        "expected": "48.612.137/0001-23",
    },
    "rayssa_nome": {
        "label": "Nome canonico Rayssa",
        "regex": r"Rayssa Pereira do Nascimento Mendes",
        "expected": "Rayssa Pereira do Nascimento Mendes",
        "wrong_variants": [
            "Rayssa Pereira Mendes do Nascimento",
            "Raissa Pereira do Nascimento Mendes",
        ],
    },
    "rayssa_cpf": {
        "label": "CPF Rayssa",
        "regex": r"355\.300\.408-88",
        "expected": "355.300.408-88",
    },
    "rayssa_percent": {
        "label": "% participacao Rayssa",
        "regex": r"Rayssa[^\n]*?(65)%",
        "expected": "65",
        "wrong_variants_regex": [
            (r"Rayssa[^\n]*?\b(45)%", "45"),
            (r"Rayssa[^\n]*?\b(27[,.]5)%", "27,5"),
        ],
    },
    "alexandre_nome": {
        "label": "Nome canonico Alexandre",
        "regex": r"Alexandre Henrique Azevedo Coleto",
        "expected": "Alexandre Henrique Azevedo Coleto",
    },
    "alexandre_percent": {
        "label": "% participacao Alexandre",
        "regex": r"Alexandre[^\n]*?(35)%",
        "expected": "35",
        "wrong_variants_regex": [
            (r"Alexandre[^\n]*?\b(27[,.]5)%", "27,5"),
        ],
    },
    "endereco_manaca": {
        "label": "Endereco Manaca (logradouro)",
        "regex": r"Av\.?\s+Rio Branco[,\s]+274",
        "expected": "Av. Rio Branco, 274 (Loja 36, Santa Lucia, Vitoria-ES, 29.056-916)",
    },
}


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse simple YAML frontmatter. Returns (frontmatter_dict, body)."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    fm_text = content[3:end].strip()
    body = content[end + 4 :].lstrip("\n")

    # Manual YAML-lite parser (handles list items + key: value)
    fm: dict = {}
    current_key = None
    for line in fm_text.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("  - ") or line.startswith("- "):
            value = line.lstrip().lstrip("- ").strip()
            if current_key:
                fm.setdefault(current_key, [])
                if isinstance(fm[current_key], list):
                    fm[current_key].append(value)
        elif ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            current_key = key
            if value:
                fm[key] = value
            else:
                fm[key] = []
    return fm, body


def load_references() -> dict[str, tuple[dict, str]]:
    """Load all references/*.md, parse frontmatter."""
    refs = {}
    for path in sorted(REFERENCES_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)
        refs[path.name] = (fm, body)
    return refs


def check_canonical_collision(refs: dict) -> list[str]:
    """Verifica se um campo canonical_for esta declarado em mais de um arquivo."""
    errors = []
    canonical_owner: dict[str, str] = {}
    for name, (fm, _) in refs.items():
        if fm.get("type") != "data":
            continue
        for field in fm.get("canonical_for", []) or []:
            if field in canonical_owner:
                errors.append(
                    f"COLISAO: campo '{field}' declarado canonical_for em "
                    f"{canonical_owner[field]} E {name}"
                )
            else:
                canonical_owner[field] = name
    return errors


def check_facts_in_text(text: str, source: str) -> list[str]:
    """Procura cada fato canonico no texto. Reporta variantes erradas."""
    errors = []
    for fact_id, fact in CANONICAL_FACTS.items():
        # Procura variantes erradas listadas
        for wrong in fact.get("wrong_variants", []):
            if wrong in text:
                errors.append(
                    f"DIVERGENCIA em {source}: encontrada variante errada "
                    f"'{wrong}' (esperado: '{fact['expected']}') | fact={fact_id}"
                )
        # Procura variantes erradas via regex
        for wrong_regex, wrong_label in fact.get("wrong_variants_regex", []):
            for m in re.finditer(wrong_regex, text):
                errors.append(
                    f"DIVERGENCIA em {source}: regex '{wrong_regex}' bateu "
                    f"-> '{m.group(0)}' (esperado: '{fact['expected']}') "
                    f"| fact={fact_id}"
                )
    return errors


def mode_refs(refs: dict) -> int:
    """Modo --refs: valida consistencia entre referencias."""
    print("=" * 60)
    print("MODO 1: Cross-check entre referencias")
    print("=" * 60)
    print(f"Carregadas {len(refs)} referencias:")
    for name, (fm, _) in refs.items():
        rtype = fm.get("type", "?")
        canonical = fm.get("canonical_for") or []
        print(f"  - {name} (type={rtype}, canonical_for={canonical})")
    print()

    errors: list[str] = []

    # 1. Colisoes de canonical_for
    errors.extend(check_canonical_collision(refs))

    # 2. Variantes erradas em qualquer arquivo
    for name, (_, body) in refs.items():
        errors.extend(check_facts_in_text(body, name))

    if errors:
        print("ERROS DETECTADOS:")
        for e in errors:
            print(f"  X {e}")
        return 1
    else:
        print("OK: todas as referencias consistentes (zero divergencias).")
        return 0


def mode_draft(refs: dict, draft_path: Path) -> int:
    """Modo --draft: valida draft contra fonte canonica."""
    print("=" * 60)
    print(f"MODO 2: Cross-check draft vs canonico")
    print(f"  Draft: {draft_path}")
    print("=" * 60)
    if not draft_path.exists():
        print(f"ERRO: arquivo nao encontrado: {draft_path}")
        return 2
    text = draft_path.read_text(encoding="utf-8")
    errors = check_facts_in_text(text, str(draft_path))

    if errors:
        print("ERROS DETECTADOS:")
        for e in errors:
            print(f"  X {e}")
        return 1
    else:
        print("OK: draft consistente com fonte canonica.")
        return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="Cross-validation de fatos canonicos da skill edital-agent."
    )
    p.add_argument(
        "--refs",
        action="store_true",
        help="Cross-check entre todas as references/*.md",
    )
    p.add_argument(
        "--draft",
        type=Path,
        help="Cross-check de um draft (markdown) contra fonte canonica",
    )
    args = p.parse_args()

    if not args.refs and not args.draft:
        p.print_help()
        return 2

    refs = load_references()
    rc = 0
    if args.refs:
        rc = max(rc, mode_refs(refs))
    if args.draft:
        rc = max(rc, mode_draft(refs, args.draft))
    return rc


if __name__ == "__main__":
    sys.exit(main())
