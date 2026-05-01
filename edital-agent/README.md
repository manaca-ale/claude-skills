# Edital Agent — Agente de Inscrição em Editais de Inovação

Skill especializada em preparar inscrições para editais de inovação, subvenção econômica, fomento à pesquisa aplicada e prêmios de empreendedorismo no Brasil, com foco operacional na **Manacá Tecnologias Sociais** (CNPJ 48.612.137/0001-23).

> Versionada no monorepo [`manaca-ale/claude-skills`](https://github.com/manaca-ale/claude-skills) na subpasta `edital-agent/`. Auto-sync ativo via bootstrap em SKILL.md a cada invocação.

---

## Para que serve

Acompanha o ciclo completo de uma inscrição em edital, do Go/No-Go ao post-mortem após o resultado. Foi construída a partir de inscrições reais (Centelha ES, Eita Recife!, Seedes, Empreendedoras Tech, Lab Procel, PES 2026, WOW Batch #34, Sebrae Startups 2026 etc.), incorporando as lições de cada uma como guia operacional ou correção factual.

## Quando ativar

Quando o usuário:

- pede para analisar, revisar ou trabalhar em um edital;
- quer preparar uma proposta/inscrição para uma chamada de fomento;
- pergunta sobre elegibilidade para um edital específico;
- pede para preencher anexos (Google Sheets/Docs) de submissão;
- menciona FAPES, FINEP, EMBRAPII, CNPq, FAPs estaduais, Sebrae Startups, Folha de S.Paulo PES, WOW;
- diz "edital", "inscrição", "proposta", "subvenção", "fomento", "prêmio";
- pede para checar, listar ou priorizar editais no ClickUp.

## Duas Trilhas

### Trilha A — Prêmio/Award (5–20h)

Formulários online, sumário executivo, pitch (vídeo/deck), PDFs de apoio. Exemplos: PES Folha, Sebrae Startups, WOW Aceleradora, Shell Iniciativa Jovem.

### Trilha B — Subvenção/Fomento (40–200h)

Anexos narrativos extensos, planilha orçamentária, protocolos com ICTs, pacotes de evidência TRL. Exemplos: FINEP/FAP, FAPESP PIPE, EMBRAPII, FAPES Nova Economia Capixaba, Lab Procel.

## Princípios fundamentais

1. **NUNCA inventar dados.** Quando faltar info, marcar `[PERGUNTAR-AO-USUÁRIO: <pergunta>]` no rascunho e perguntar antes de finalizar. Esta regra é **fiduciária** — violá-la custa credibilidade da CEO frente a banca de avaliadores. Detalhes em SKILL.md §"Regra Absoluta".
2. **Português brasileiro completo desde o primeiro rascunho.** Acentuação, formatação R$ X.XXX,XX, datas por extenso. Não é polish final — é parte da qualidade.
3. **Local-first.** Drafting em arquivos locais (`c:\Editais\editais\<slug>\`). Google Docs e plataformas de submissão entram apenas no fim, ou conforme exigência.
4. **Validar fatos antes de submeter.** Rodar `python scripts/validate_facts.py --refs` na Fase 2.5 e na 5a.0 (Audit de Lacunas).
5. **Sempre referenciar inscrições anteriores.** Vencedoras em `c:\Editais\00. Vencedores\`, submetidas aguardando resultado em `c:\Editais\01. Submetidos\`.

## Estrutura da skill

```
edital-agent/
├── SKILL.md                               # Spec completa: 8 fases, 2 trilhas, bootstrap, regra "Nunca Inventar"
├── README.md                              # Este arquivo
├── references/                            # Banco factual + guias operacionais
│   ├── empresa-manaca.md                  # CNPJ, sócios, financeiro, certidões, PI
│   ├── equipe.md                          # CVs detalhados, idiomas, diversidade
│   ├── projeto-flora.md                   # SaaS impacto: TAM/SAM/SOM, pricing, ICP
│   ├── projeto-saira.md                   # CPSI Recife, YOLO v8/v11, modelo receita
│   ├── historico-financiamentos.md        # 8 editais vencidos + inscrições em andamento
│   ├── classificacao-financeira-editais.md # Faturamento vs captação, pró-labore, % produto
│   ├── guia-redacao-editais.md            # Tom, estrutura, TRL, SMART budget, exemplos canônicos
│   ├── guia-equipe-editais.md             # Tripé de avaliação, red flags, checklist de 8 perguntas
│   ├── matriz-agencias-equipe.md          # Regras por agência (FINEP/FAPESP/EMBRAPII/FAPs/Prêmios)
│   ├── mapeamento-formularios-playwright.md # Workflow para mapear formulários com login
│   ├── clickup-editais.md                 # IDs workspace, status mapping, integração
│   └── gotchas-editais.md                 # Pegadinhas práticas (Drive API, auth, PT-BR, login, etc.)
├── templates/equipe/                      # 5 templates: súmula, matriz competências, ICTs, etc.
└── scripts/                               # Utilidades Python
    ├── parse_edital_pdf.py                # Extrai estrutura de edital PDF
    ├── clickup_edital_sync.py             # Integração ClickUp (UTF-8 safe)
    ├── drive_auth.py / upload_to_drive.py # Auth + upload Drive (Shared Drive aware)
    ├── reorganize_drive.py                # Reorganiza pasta do edital em layout padrão
    ├── update_docs_content.py             # Atualiza Google Docs preservando fileId/link
    ├── validate_facts.py                  # Cross-check de fatos canônicos + lacunas pendentes
    └── accent_guard.py                    # Sanity check de acentuação (não corrige, só sinaliza)
```

## Workflow das 8 Fases

| Fase | Output | Trilha A | Trilha B |
|------|--------|----------|----------|
| 0 — Triagem (Go/No-Go) | `00-triage.md` | obrigatória | obrigatória |
| 1 — Ingestão do edital | `01-edital-parsed.md` | obrigatória | obrigatória |
| 2 — Elegibilidade | `02-eligibility.md` | combinável com Fase 1 | obrigatória |
| 2.5 — Validação de fatos canônicos | `02b-data-validation.md` | obrigatória | obrigatória |
| 3 — Sugestão de projeto | `03-project-suggestion.md` | obrigatória | obrigatória |
| 4 — Planejamento de docs | `04-document-plan.md` | opcional | obrigatória |
| 5a — Data Assembly (com 5a.0 Audit de Lacunas) | `05a-data-pack.md` | obrigatória | obrigatória |
| 5b — Narrativa Core | `05b-narrativa-*.md` | (parte do produção direta) | obrigatória |
| 5c — Seções de suporte (equipe, cronograma, PI) | `05c-*.md` | parcial | obrigatória |
| 5d — Orçamento | `05d-orcamento.md` | — | obrigatória |
| 5e — Integração + Polish | `05e-documento-final.md` | obrigatória | obrigatória |
| 6 — Revisão (advocate + red team) | `06-quality-review.md` | obrigatória | obrigatória |
| 7 — Guia de submissão (Caderno de Preenchimento) | `07-submission-guide.md` | obrigatória | obrigatória |
| 8 — Post-mortem após resultado | `08-post-mortem.md` | quando sair resultado | quando sair resultado |

## Referência factual canônica (atualizada mai/2026)

| Campo | Valor |
|-------|-------|
| Razão Social | MANACA TECNOLOGIAS SOCIAIS LTDA |
| CNPJ | 48.612.137/0001-23 |
| Sede | Av Rio Branco, 274, Loja 36, Santa Lúcia, Vitória-ES, CEP 29.056-916 |
| Sócios | Rayssa Mendes (CEO 65%) + Alexandre Coleto (CTO 35%) — após saída Ângelo Viana em 05/09/2025 |
| Equipe fixa | 7 (2 sócios + 5 colaboradores) + 2 consultores acionáveis |
| Faturamento acumulado | R$ 646.915,17 (até mai/2026) |
| Crescimento médio anual | 140% |
| Atuação | 14 municípios em 11 estados, 3 regiões |
| Captação via editais | R$ 255.600,00 (Centelha ES + NIS + Seedes + Empreendedoras Tech) |
| Projetos âncora | Flora (SaaS gestão de impacto) + SAÍRA (CPSI Recife — smart city resíduos) |

## Manutenção

- Cada arquivo em `references/` tem frontmatter com `last_verified` e `next_review`.
- Rodar `python scripts/validate_facts.py --refs` antes de cada uso para detectar divergências entre arquivos canônicos e listar lacunas pendentes (`[PERGUNTAR-AO-USUÁRIO]` / `[PREENCHER]`).
- Após cada edital concluído, atualizar referências com lições aprendidas (Fase 8 — Consolidação Final).

## Histórico de versões

- **2026-05** — Major update após 3 inscrições (PES 2026, WOW Batch #34, Sebrae Startups 2026): regra "Nunca Inventar Dados", convenção `[PERGUNTAR-AO-USUÁRIO]`, sub-fase 5a.0, 10 exemplos canônicos de redação, atualização de pricing Flora (3 planos), TAM/SAM/SOM, modelos YOLO v8/v11, telefone CEO, novos selos (PMI-ES, Portal Impacta MDIC).
- **2026-04** — Lições do Lab Procel: convenção `canonical_for` no frontmatter, `validate_facts.py --refs` na Fase 2.5, validação de certidões na Fase 2 (não na 7), critique do deliverable não do notepad, índice de ativos reutilizáveis em `projeto-*.md`.

## Licença / Uso

Skill pessoal/operacional para a Manacá Tecnologias Sociais. O conteúdo de `references/` contém dados sensíveis (CNPJ, CPF, faturamento, contatos) que **não devem ser compartilhados** fora do contexto da empresa.

## Suporte

Issues, sugestões e melhorias: https://github.com/manaca-ale/claude-skills/issues
