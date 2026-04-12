#!/usr/bin/env python3
"""
Extract structured sections from a Brazilian edital (public tender) PDF.

Usage:
    python parse_edital_pdf.py <pdf_path> [output_path]

Outputs a structured markdown file with:
- Metadata (agency, program, dates, values)
- Eligibility criteria
- Evaluation criteria with weights
- Required documents (annexes)
- Financial parameters
- Timeline
"""

import sys
import re
import pdfplumber


def extract_text(pdf_path: str) -> str:
    """Extract all text from PDF."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n\n".join(pages)


def find_section(text: str, patterns: list[str], next_patterns: list[str] = None) -> str:
    """Find text between a section header pattern and the next section."""
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            start = match.start()
            # Find the end (next major section)
            end = len(text)
            if next_patterns:
                for np in next_patterns:
                    next_match = re.search(np, text[match.end():], re.IGNORECASE | re.MULTILINE)
                    if next_match:
                        end = min(end, match.end() + next_match.start())
            return text[start:end].strip()
    return ""


def extract_values(text: str) -> dict:
    """Extract financial values from text."""
    values = {}

    # Look for R$ amounts
    amounts = re.findall(r'R\$\s*([\d.,]+)', text)
    if amounts:
        values['amounts_found'] = amounts

    # Look for percentage patterns
    percentages = re.findall(r'(\d+(?:,\d+)?)\s*%', text)
    if percentages:
        values['percentages_found'] = percentages

    # Look for duration
    duration = re.findall(r'(\d+)\s*(?:meses|months)', text, re.IGNORECASE)
    if duration:
        values['duration_months'] = duration

    return values


def extract_dates(text: str) -> list[str]:
    """Extract relevant dates from text."""
    # Brazilian date patterns
    dates = re.findall(
        r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}|\d{2}/\d{2}/\d{4}|\d{2}\.\d{2}\.\d{4}',
        text
    )
    return dates


def parse_edital(pdf_path: str) -> str:
    """Parse an edital PDF into structured markdown."""
    text = extract_text(pdf_path)

    if not text:
        return "# Error\n\nCould not extract text from PDF."

    # Build structured output
    output = []
    output.append(f"# Edital Parsed: {pdf_path.split('/')[-1]}\n")

    # --- METADATA ---
    output.append("## 1. Metadados\n")

    # Try to find agency/program name (usually in first 500 chars)
    header = text[:1000]
    output.append(f"**Primeiras linhas do edital:**\n```\n{header[:500]}\n```\n")

    # Extract dates
    dates = extract_dates(text)
    if dates:
        output.append(f"**Datas encontradas:** {', '.join(dates[:10])}\n")

    # Extract financial values
    values = extract_values(text)
    if values.get('amounts_found'):
        output.append(f"**Valores financeiros (R$):** {', '.join(values['amounts_found'][:10])}\n")
    if values.get('duration_months'):
        output.append(f"**Duração (meses):** {', '.join(values['duration_months'])}\n")

    # --- OBJECTIVE ---
    output.append("\n## 2. Objetivo\n")
    obj_section = find_section(text,
        [r'(?:DO\s+)?OBJETIVO', r'OBJETO\b', r'FINALIDADE'],
        [r'\d+\.\s+D[OA]\s', r'REQUISITOS', r'ELEGIB']
    )
    if obj_section:
        output.append(obj_section[:2000] + "\n")

    # --- ELIGIBILITY ---
    output.append("\n## 3. Elegibilidade e Requisitos\n")
    elig_section = find_section(text,
        [r'ELEGIB', r'REQUISITOS\s+(?:DE\s+)?(?:PARTICIPAÇÃO|HABILITAÇÃO)',
         r'QUEM\s+PODE\s+PARTICIPAR', r'CONDIÇÕES\s+DE\s+PARTICIPAÇÃO'],
        [r'AVALIAÇÃO', r'CRITÉRIOS\s+DE\s+(?:MÉRITO|JULGAMENTO)', r'CRONOGRAMA']
    )
    if elig_section:
        output.append(elig_section[:3000] + "\n")

    # --- EVALUATION CRITERIA ---
    output.append("\n## 4. Critérios de Avaliação\n")
    eval_section = find_section(text,
        [r'CRITÉRIOS\s+DE\s+(?:AVALIAÇÃO|MÉRITO|JULGAMENTO|SELEÇÃO)',
         r'ANÁLISE\s+DE\s+MÉRITO'],
        [r'CONTRATAÇÃO', r'RECURSOS\s+FINANCEIROS', r'CRONOGRAMA', r'ANEXO']
    )
    if eval_section:
        output.append(eval_section[:3000] + "\n")

    # --- FINANCIAL PARAMETERS ---
    output.append("\n## 5. Parâmetros Financeiros\n")
    fin_section = find_section(text,
        [r'RECURSOS\s+FINANCEIROS', r'VALOR\s+(?:MÁXIMO|DO\s+APOIO)',
         r'ORÇAMENTO', r'FINANCIAMENTO', r'INVESTIMENTO'],
        [r'CRONOGRAMA', r'ANEXO', r'DISPOSIÇÕES']
    )
    if fin_section:
        output.append(fin_section[:2000] + "\n")

    # --- TIMELINE ---
    output.append("\n## 6. Cronograma / Prazos\n")
    timeline_section = find_section(text,
        [r'CRONOGRAMA', r'PRAZOS', r'CALENDÁRIO', r'FLUXO\s+DE\s+SUBMISSÃO'],
        [r'ANEXO', r'DISPOSIÇÕES\s+(?:GERAIS|FINAIS)']
    )
    if timeline_section:
        output.append(timeline_section[:2000] + "\n")

    # --- REQUIRED DOCUMENTS / ANNEXES ---
    output.append("\n## 7. Documentos e Anexos Necessários\n")

    # Find all ANEXO references
    annexes = re.findall(r'ANEXO\s+[IVX]+\s*[-–:]\s*([^\n]+)', text, re.IGNORECASE)
    if annexes:
        for i, annex in enumerate(annexes):
            output.append(f"- **ANEXO {['I','II','III','IV','V','VI','VII','VIII','IX','X'][i] if i < 10 else i+1}:** {annex.strip()}")
        output.append("")

    # --- FULL TEXT (for reference) ---
    output.append("\n## 8. Texto Completo (Referência)\n")
    output.append(f"Total de caracteres extraídos: {len(text)}\n")
    output.append(f"Para consulta completa, ver o PDF original.\n")

    return "\n".join(output)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_edital_pdf.py <pdf_path> [output_path]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else pdf_path.rsplit('.', 1)[0] + '-parsed.md'

    result = parse_edital(pdf_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"Parsed edital saved to: {output_path}")
    print(f"Total output: {len(result)} characters")
