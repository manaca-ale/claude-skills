---
name: saira-relatorio-mensal
description: >
  Gera o Relatório de Atividades Mensais do projeto SAÍRA (Prefeitura do Recife / EMPREL).
  Esta skill deve ser usada quando o usuário pedir para criar o relatório mensal do SAÍRA,
  passando os artefatos desenvolvidos nas sprints do mês e os equipamentos comprados.
  Ela copia o último relatório existente no Google Drive como template, atualiza todo o
  conteúdo (atividades, artefatos, equipamentos, resumo financeiro) e entrega o link do
  novo documento editável.
---

# SAIRA – Gerador de Relatório de Atividades Mensais

Gerar o relatório mensal copiando o último relatório existente como template e substituindo
o conteúdo com os dados do mês corrente fornecidos pelo usuário.

## Configuração fixa

- **Google email**: `contato@manaca.tech`
- **Planilha de escopo/valores**: ID `14-0S114IUxMfJgOlY_jidzHU5k5e5U6xVgLEAPeVggI`, aba `ESCOPO MVP AJUSTADO V2`
- **Nome do novo doc**: `Relatório de Atividades Mensais [Mês]/[Ano] - Projeto SAÍRA`

## Inputs esperados do usuário

Ao acionar a skill, coletar (se não informados na mensagem):

1. **Mês/Ano** do relatório (ex: `Março/2026`)
2. **Sprints do mês**: para cada sprint — período, atividades entregues, CAs endereçados
3. **Artefatos**: ID, nome, tipo (PDF / FIGMA / etc.), localização
4. **Equipamentos comprados**: lista de itens com quantidade e valor (pode ser texto bruto das NFs)
5. **ID do último relatório** (se souber); caso contrário, buscar com:
   ```
   search_drive_files(query="name contains 'Relatório de Atividades Mensais' and mimeType='application/vnd.google-apps.document'")
   ```

## Workflow passo a passo

### 1. Ler o template

Usar `get_doc_as_markdown` no último relatório para mapear os textos exatos a substituir.

### 2. Ler valores das sprints

Usar `read_sheet_values` na aba `ESCOPO MVP AJUSTADO V2` para localizar valores das atividades do mês.
Calcular:
- Valor de cada sprint = soma das atividades da sprint na coluna de custo
- Total Equipamentos = soma dos itens informados pelo usuário
- **Total Mês = Σ(Sprints) + Equipamentos**

### 3. Copiar o template

```
copy_drive_file(
  file_id=<id_ultimo_relatorio>,
  new_name="Relatório de Atividades Mensais [Mês]/[Ano] - Projeto SAÍRA"
)
```

Guardar o `file_id` do novo documento.

### 4. Inspecionar estrutura

Usar `inspect_doc_structure(detailed=True)` e `get_doc_as_markdown` para mapear o conteúdo atual.

### 5. Substituições com find_and_replace

Executar `find_and_replace_doc` para cada trecho a atualizar. **Regras críticas:**

- Substituir um trecho por vez (multiline falha)
- **NUNCA usar `match_case: false` quando o termo contiver "Print"** — corruprá todas as ocorrências de "Sprint" (substring match). Sempre usar `match_case: true` nesses casos
- Para remover texto: `replace_text: ""`
- Se retornar 0 replacements: o texto está em múltiplos runs — usar `modify_doc_text` com insert no `insertion_index`

**Ordem de substituições:**

| Encontrar | Substituir |
|-----------|-----------|
| Mês/Ano na capa (ex: `Jan/2026`) | Novo mês/ano |
| Parágrafo da Introdução (seção 1) | Novo contexto do mês |
| Parágrafo intro da seção 4 | Resumo das sprints |
| Título 4.1 | Primeira sprint/atividade |
| Corpo 4.1 (descrição + Atividade Chave) | Conteúdo da sprint |
| CAs da 4.1 | CAs endereçados |
| Título 4.2 | Segunda sprint |
| Corpo 4.2 | Conteúdo |
| Título 4.3 | Terceira sprint (se houver) |
| Corpo 4.3 | Conteúdo |
| Corpo seção 4.5 (Equipamentos) | Lista de itens com valores |
| Pontos de Atenção (seção 5) | Riscos e impedimentos atuais |
| Parágrafo Conclusão (seção 6) | Nova conclusão |
| `Resumo Financeiro - Mês N` | `Resumo Financeiro - Mês [N+1]` |
| Linha `Valor da Sprint X: R$ Y` | Novas linhas com valores corretos |
| Linha `Aquisição de Equipamentos: R$ X` | Novo total de equipamentos |
| Linha `Valor Total do Mês N: R$ X` | Novo total |
| Data de assinatura | Nova data |

**Manter inalteradas:** Seção 2 (Empresa) e Seção 3 (Critérios de Aceite).

### 6. Atualizar tabela de artefatos (seção 4.4)

Usar `debug_table_structure(table_index=1)` para obter `insertion_index` de cada célula.

**Regras para editar células de tabela:**

- Para **adicionar** conteúdo a células vazias: `modify_doc_text(start_index=insertion_index, text="conteúdo")` sem `end_index` (insert puro)
- Para **substituir** conteúdo existente: preferir `find_and_replace_doc` com o texto exato
- **Nunca** usar `modify_doc_text` com `end_index` cobrindo o `\n` de parágrafo — retorna `Invalid deletion range`
- Modificar **de baixo para cima** (maior índice primeiro) para evitar drift
- Re-executar `debug_table_structure` após qualquer inserção que altere tamanho do texto

**Estrutura esperada da tabela de artefatos:**

| ID | Artefato | Tipo | Link de Acesso / Localização |
|----|----------|------|------------------------------|
| ART-01 | Nome do artefato | PDF / FIGMA | Localização ou link |
| ART-02 | ... | ... | ... |
| ... | ... | ... | ... |

### 7. Verificação final

Usar `get_doc_as_markdown` e confirmar:

- [ ] Capa com mês/ano correto
- [ ] Introdução atualizada com as sprints do mês
- [ ] Seções 4.1, 4.2, 4.3 com conteúdo correto
- [ ] Tabela de artefatos com IDs, nomes, tipos e links
- [ ] Seção 4.5 com lista de equipamentos e total
- [ ] Seção 5 com pontos de atenção atualizados
- [ ] Resumo Financeiro com valores e total corretos
- [ ] Data de assinatura correta
- [ ] Seções 2 e 3 **inalteradas**

Entregar o link do documento ao usuário.

## Armadilhas conhecidas

| Problema | Causa | Solução |
|----------|-------|---------|
| "Sprint" vira "SPDF" | `find_and_replace` case-insensitive em "Print" | Usar `match_case: true` sempre que o termo contiver "Print" |
| `find_and_replace` retorna 0 replacements | Texto em múltiplos runs (negrito, links, formatação) | Usar `modify_doc_text` insert no `insertion_index` do parágrafo/célula |
| `modify_doc_text` retorna `Invalid deletion range` | Range inclui `\n` estrutural da célula | Usar insert puro (sem `end_index`) ou `find_and_replace` |
| Inserção vai para célula errada na tabela | Índices stale após outras inserções | Re-debugar tabela antes de cada insert; sempre modificar de baixo para cima |
| Conteúdo de células misturado (text garbled) | Inserções em índices desatualizados | Re-debug após cada insert; corrigir com `find_and_replace` da string resultante visível no debug |
| PDF do Drive via MCP retorna conteúdo corrompido | Download MCP é inválido | Ler PDFs diretamente do Google Drive File Stream montado em `H:\Drives compartilhados\...` via PyMuPDF |

## Estrutura do relatório (referência)

```
Capa:        "Projeto SAIRA\nRelatório mensal\n[Mês/Ano]"
Seção 1:     INTRODUÇÃO — contexto do mês, sprints cobertas, entregas
Seção 2:     APRESENTAÇÃO DA EMPRESA — manter sem alteração
Seção 3:     CRITÉRIOS DE ACEITE — manter sem alteração
Seção 4:     DETALHAMENTO DAS ATIVIDADES E ENTREGÁVEIS
  4.intro:     Parágrafo descrevendo as sprints do mês
  4.1:         [Sprint/Atividade 1] título + corpo + Atividade Chave + Status + CAs
  4.2:         [Sprint/Atividade 2]
  4.3:         [Sprint/Atividade 3]
  4.4:         Artefatos desenvolvidos (tabela 5×4)
  4.5:         Registro de Equipamentos (lista bullet com itens e valores)
Seção 5:     PONTOS DE ATENÇÃO, RISCOS OU IMPEDIMENTOS
Seção 6:     CONCLUSÃO
  6.body:      Parágrafo de conclusão
  6.financ:    Resumo Financeiro - Mês N
               - Valor da Sprint X: R$ Y
               - Aquisição de Equipamentos: R$ Z
               - Valor Total do Mês N: R$ TOTAL
  6.date:      [Cidade], [DD] de [Mês] de [Ano].
  6.sign:      Rayssa Pereira do Nascimento Mendes / CEO
```
