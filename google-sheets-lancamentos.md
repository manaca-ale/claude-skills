---
name: google-sheets-lancamentos
description: Insert financial rows in the fixed Google Sheet `1CtGEokgGb_TMIua4KvYjDyQoIyq9Cpuav987WF1BSRc` and tab `lancamentos`, asking for launch fields and writing with Google Sheets tools. Use for new launches, installment splits (`1/x`, `2/x`, ...), and fast dry-run/apply flows with preflight checks.
---

# Google Sheets Lancamentos

Use this exact target:
- `spreadsheet_id`: `1CtGEokgGb_TMIua4KvYjDyQoIyq9Cpuav987WF1BSRc`
- `sheet_name`: `lancamentos`

## Inputs To Ask User

Always ask:
- `Mes`
- `N de parcelas`
- `Valor total`
- `Item`
- `Categoria`
- `Receita ou Despesa`
- `Data da compra`
- `Pagador`

## Fast Default Path

Use the script at `C:/Users/aleco/.codex/skills/google-sheets-lancamentos/scripts/lancar_lancamentos.py`.

Example (dry-run):

```bash
python "C:/Users/aleco/.codex/skills/google-sheets-lancamentos/scripts/lancar_lancamentos.py" \
  --user-google-email alecoleto@gmail.com \
  --mes "11 - Novembro" \
  --parcelas 3 \
  --valor-total "1200,00" \
  --item "Hospedagem evento" \
  --categoria "Viagens e eventos" \
  --tipo "Despesa" \
  --data-compra "26/02/2026" \
  --pagador "Cartao de credito"
```

Apply write:

```bash
python "C:/Users/aleco/.codex/skills/google-sheets-lancamentos/scripts/lancar_lancamentos.py" ... --apply
```

Fast mode (skip read-back verification):

```bash
python "C:/Users/aleco/.codex/skills/google-sheets-lancamentos/scripts/lancar_lancamentos.py" ... --apply --fast-mode
```

## Performance Rules

1. Run preflight fail-fast before any write.
   Check tools, sheet name, and locale.

2. Normalize locale-sensitive values.
   Use `pt_BR` decimal format (`99,99`).

3. Preserve existing formatting from the sheet.
   When shifting rows, read current values from Google Sheets and write them back shifted.
   Do not rebuild shifted rows from raw XLSX numeric/date values.

4. Default to dry-run.
   Show planned target rows and values before writing.

5. Use decimal comma for all inserted numeric values.
   Write `Valor total` and `Valor unitario` as strings like `1585,90` and `158,59`.

6. Use `--fast-mode` only when user requests speed over strict verification.

## Insertion Logic

1. Locate the last row for the month in column `B`.
2. Place the new row at the first free row at or below that anchor.
3. For installments, expand month by month and create `1/x`, `2/x`, ... `x/x`.
