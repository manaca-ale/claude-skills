---
last_verified: 2026-04-14
next_review: 2026-07-14
type: data
canonical_for:
  - clickup_workspace_ids
  - clickup_lista_editais_id
  - clickup_status_editais
derived_from: []
---

# ClickUp — Editais Integration Reference

## Workspace Structure (IDs fixos)

| Resource | Name | ID |
|----------|------|----|
| Workspace | Manaca | `90132913705` |
| Space | Manaca | `901312961048` |
| Folder | Captacao de recursos e premiacoes | `901316670330` |
| List | Editais | `901324801079` |

## Status Mapping

| ClickUp Status | Edital-Agent Phase | Action |
|----------------|-------------------|--------|
| `a fazer` | Pre-triagem | Edital cadastrado, aguardando analise |
| `claude` | Fases 1-5 (Producao) | Em trabalho ativo pelo Claude |
| `revisao` | Fase 6 (Quality Review) | Conteudo pronto, em revisao |
| `subir para o drive` | Fase 5e -> Drive | Docs prontos, falta arquivar no Drive |
| `em andamento` | Ativo (equipe humana) | Equipe trabalhando (nao Claude) |
| `parado` | Bloqueado | Dependencia externa ou decisao pendente |
| `complete` | Concluido | Submetido ou arquivado |
| `cancelled` | Cancelado | No-Go ou prazo perdido |

## Tags Relevantes

| Tag | Significado |
|-----|------------|
| `claude` | Tarefa sendo tratada pelo Claude |
| `urgente` | Prazo iminente (< 7 dias) |
| `priorizar` | Alta prioridade estrategica |

## Helper Script

```bash
# Located at: scripts/clickup_edital_sync.py
python scripts/clickup_edital_sync.py list              # Listar editais ativos
python scripts/clickup_edital_sync.py get <task_id>     # Detalhes completos
python scripts/clickup_edital_sync.py links <task_id>   # Extrair links e anexos
python scripts/clickup_edital_sync.py status <id> <st>  # Atualizar status
python scripts/clickup_edital_sync.py comment <id> <tx> # Adicionar comentario
python scripts/clickup_edital_sync.py create <name> [dd/mm/yyyy] # Criar tarefa
```

## Credentials

- Token: `C:/secrets/Envs/envclickuptelegram` (CLICKUP_ACCESS_TOKEN)
- Auto-setup: script clona e desbloqueia o repo Envs automaticamente

## Important Notes

- **SEMPRE usar Python `requests`** para comentarios (nunca curl) — evita mojibake com acentos
- **Links ficam no `markdown_description`**, NAO no `description` — sempre buscar com `?include_markdown_description=true`
- **Attachments** ficam no campo `attachments` da resposta da API
- **Free plan**: 5/5 spaces, 100 automations/month, sem custom fields avancados
