#!/usr/bin/env python3
"""accent_guard.py — Detecta palavras canonicas sem acento em deliverables PT-BR.

Caso real (Lab Procel): geracao automatica produz "Manaca", "Saira", "Vitoria" no
lugar de "Manaca", "SAIRA", "Vitoria". Este script:

1. Constroi dicionario de palavras canonicas com acento, derivado dinamicamente
   das references/*.md (qualquer palavra com acento aparece como canonica).
2. Mapeia para a forma sem acento (chave de busca).
3. Escaneia o(s) arquivo(s) alvo procurando pela forma sem acento.
4. Reporta cada ocorrencia. **Nao corrige automaticamente** — substituir cego
   quebra nomes proprios ("Marco Legal" -> "Marco Legal", incorreto).

Uso:
    python accent_guard.py <path>              # checa um arquivo
    python accent_guard.py --pdf <path>        # extrai texto de PDF e checa
    python accent_guard.py --dir <pasta>       # checa todos os .md de uma pasta

Exit code 0 se zero hits; 1 se houver suspeita.

Dependencias: pypdf (opcional, so com --pdf).
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

REFERENCES_DIR = Path(__file__).resolve().parent.parent / "references"

# Exception list: palavras que NAO devem ser sinalizadas mesmo sendo
# variante sem acento de alguma palavra canonica. Caso "Marco" (palavra
# real) vs "Marco" (do "Marco Legal das Startups"). Adicione conforme
# encontrar falsos positivos.
EXCEPTIONS = {
    # Termos onde a versao sem acento e valida em algum contexto
    "marco",       # "Marco Legal das Startups" — palavra valida sem acento
    "lab",         # "Lab Procel"
    "procel",
    "senai",
    "enbpar",
    "fgts",
    "cnpj",
    "cpf",
    "saira",       # tolerado em URL/file paths
    "manaca",      # idem
    "petrobras",   # tanto Petrobras quanto Petrobrás sao validos
    "natura",      # vs Naturá (raro)
    # Palavras curtas comuns em PT-BR onde sem acento e valido
    "pre",         # "pre-" prefixo, ou "pre" (forma comum em codigo)
    "pro",         # "pro" colquial vs "Pró"
    "for",
    "para",
    "data",
    "type",
    "do",
    "de",
    "no",
    "nos",
    "pos",         # "pos-" prefixo
}


def strip_accents(s: str) -> str:
    """Remove acentos de uma string (NFD + filtra combining)."""
    nfd = unicodedata.normalize("NFD", s)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def build_dict_from_refs(refs_dir: Path, min_len: int = 5) -> dict[str, str]:
    """
    Constroi dict {forma_sem_acento_lowercase: forma_canonica_com_acento}
    extraindo palavras com acento das referencias.

    Filtros para reduzir falsos positivos:
    - Apenas palavras com pelo menos `min_len` chars (default 5) OU
      palavras que comecam com maiuscula (nomes proprios)
    - Pula palavras na EXCEPTIONS list
    """
    accent_pattern = re.compile(
        r"\b\w*[à-ÿÀ-ß]\w*\b", re.UNICODE
    )
    canonical: dict[str, str] = {}
    for path in refs_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        for m in accent_pattern.finditer(text):
            word = m.group(0)
            # Filtro: tamanho minimo OU primeira letra maiuscula
            if len(word) < min_len and not word[0].isupper():
                continue
            key = strip_accents(word).lower()
            if key in EXCEPTIONS:
                continue
            # Mantem primeira forma vista (presumindo referencias bem escritas)
            canonical.setdefault(key, word)
    return canonical


def scan_file(path: Path, canonical: dict[str, str]) -> list[tuple[int, int, str, str]]:
    """
    Procura ocorrencias da forma sem acento no arquivo.
    Retorna lista de (linha, coluna, encontrado, sugestao_canonica).
    """
    text = path.read_text(encoding="utf-8")
    hits: list[tuple[int, int, str, str]] = []
    word_pat = re.compile(r"\b[A-Za-z][A-Za-z]+\b")
    lines = text.splitlines()
    for line_no, line in enumerate(lines, start=1):
        for m in word_pat.finditer(line):
            word = m.group(0)
            if word.lower() in EXCEPTIONS:
                continue
            # Filtro: ignora palavras curtas que nao sao nomes proprios
            if len(word) < 5 and not word[0].isupper():
                continue
            # Se a palavra ja tem acento, nao e candidata a problema
            if any(ord(c) > 127 for c in word):
                continue
            key = word.lower()
            if key in canonical:
                # Confirma que a versao canonica TEM acento (senao nao e suspeita)
                cano = canonical[key]
                if cano.lower() == word.lower():
                    continue  # mesma forma, nao e divergencia
                hits.append((line_no, m.start() + 1, word, cano))
    return hits


def scan_pdf(path: Path, canonical: dict[str, str]) -> list[tuple[int, int, str, str]]:
    """Extrai texto de PDF e roda scan_file equivalente em memoria."""
    try:
        from pypdf import PdfReader
    except ImportError:
        print("ERRO: pypdf nao instalado. Instale: pip install pypdf")
        sys.exit(2)

    r = PdfReader(str(path))
    full_text = "\n".join((p.extract_text() or "") for p in r.pages)
    # Reusa logica do scan_file mas com texto em memoria
    hits: list[tuple[int, int, str, str]] = []
    word_pat = re.compile(r"\b[A-Za-z][A-Za-z]+\b")
    lines = full_text.splitlines()
    for line_no, line in enumerate(lines, start=1):
        for m in word_pat.finditer(line):
            word = m.group(0)
            if word.lower() in EXCEPTIONS:
                continue
            if len(word) < 5 and not word[0].isupper():
                continue
            if any(ord(c) > 127 for c in word):
                continue
            key = word.lower()
            if key in canonical:
                cano = canonical[key]
                if cano.lower() == word.lower():
                    continue
                hits.append((line_no, m.start() + 1, word, cano))
    return hits


def report(path: Path, hits: list[tuple[int, int, str, str]]) -> None:
    if not hits:
        print(f"OK {path}: 0 hits")
        return
    print(f"AVISO {path}: {len(hits)} ocorrencias suspeitas:")
    # Agrupa por (encontrado, sugestao)
    grouped: dict[tuple[str, str], list[tuple[int, int]]] = {}
    for line, col, w, cano in hits:
        grouped.setdefault((w, cano), []).append((line, col))
    for (w, cano), positions in sorted(grouped.items()):
        first_pos = positions[0]
        rest = "" if len(positions) == 1 else f" (+{len(positions) - 1} outras)"
        print(f"  [{first_pos[0]}:{first_pos[1]}] '{w}' -> sugestao: '{cano}'{rest}")


def main() -> int:
    p = argparse.ArgumentParser(description="Detecta palavras sem acento (PT-BR).")
    p.add_argument("path", type=Path, nargs="?", help="Arquivo .md a verificar")
    p.add_argument(
        "--pdf", type=Path, help="Extrai texto de PDF e verifica acentos"
    )
    p.add_argument(
        "--dir",
        type=Path,
        help="Verifica todos os .md de uma pasta (recursivo)",
    )
    p.add_argument(
        "--refs-dir",
        type=Path,
        default=REFERENCES_DIR,
        help="Pasta de referencias para construir dicionario canonico",
    )
    args = p.parse_args()

    if not (args.path or args.pdf or args.dir):
        p.print_help()
        return 2

    canonical = build_dict_from_refs(args.refs_dir)
    print(f"Dicionario canonico: {len(canonical)} palavras com acento "
          f"(derivado de {args.refs_dir})")
    print()

    rc = 0
    if args.path:
        hits = scan_file(args.path, canonical)
        report(args.path, hits)
        if hits:
            rc = 1

    if args.pdf:
        hits = scan_pdf(args.pdf, canonical)
        report(args.pdf, hits)
        if hits:
            rc = 1

    if args.dir:
        for md in sorted(args.dir.rglob("*.md")):
            hits = scan_file(md, canonical)
            if hits:
                rc = 1
            report(md, hits)

    return rc


if __name__ == "__main__":
    sys.exit(main())
