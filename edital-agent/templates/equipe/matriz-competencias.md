# Matriz de Competências × Metas × TRL

**Uso:** preencher na Fase 05c.2 para evidenciar sinergia da equipe ao avaliador. Anexar à narrativa da seção de equipe ou usar como insumo para gerar a redação.

**Princípio:** o avaliador não deve precisar adivinhar como o time interage. A matriz torna explícito que cada pessoa tem um papel claro, cada meta tem responsável definido, e os handoffs entre pessoas estão mapeados.

---

## Tabela A — Membro × Meta × TRL × Competência-chave

| Membro | Papel no Projeto | Metas que Lidera | TRL alvo | Competência-chave aplicada |
|---|---|---|---|---|
| {NOME} | {PR / Coordenador / CTO / Pesquisador / PO} | M1, M2 | TRL {X} → {Y} | {stack + metodologia específica} |
| {NOME} | {...} | M3 | TRL {X} → {Y} | {...} |
| {NOME} | {...} | M4, M5 | TRL {X} → {Y} | {...} |

**Exemplo preenchido (SAIRA — lab-procel):**

| Membro | Papel | Metas | TRL alvo | Competência-chave |
|---|---|---|---|---|
| Alexandre Coleto | CTO / Líder Técnico | M1 (arquitetura), M2 (pipeline IA) | TRL 4 → 6 | Arquitetura cloud + visão computacional YOLO + orquestração de agentes |
| Gabriel Candelaria | Engenheiro de IA | M2 (modelo de detecção) | TRL 4 → 5 | Deep learning (CNN/YOLO), TensorFlow, OpenCV |
| Gabrielle Alves | Product Designer | M3 (dashboard gestão pública), M4 (app denúncia) | TRL 5 → 6 | UX para IA + pesquisa com gestores públicos |
| Rafaela Rezende | Product Owner / Eng. Dados de Impacto | M3 (indicadores), M5 (mensuração E2.1) | TRL 5 → 7 | Mensuração de impacto + Scrum/Lean + ESG |
| Rayssa Mendes | CEO / Coordenadora Geral | M1 (governança), M6 (articulação com Prefeitura), M7 (disseminação) | TRL 6 → 7 | Articulação pública + captação + gestão de stakeholders |

---

## Tabela B — Handoffs entre Membros (cadeia de P&D)

| De → Para | O que é entregue (insumo) | Quando (mês do cronograma) | Critério de aceite |
|---|---|---|---|
| {A} → {B} | {entregável} | M{X} | {critério técnico} |
| {B} → {C} | {entregável} | M{Y} | {...} |

**Exemplo preenchido:**

| De → Para | Entregável | Mês | Aceite |
|---|---|---|---|
| Alexandre → Gabriel | Arquitetura de dados + dataset anotado | M1 | Dataset com 10K imagens + anotações YOLO |
| Gabriel → Gabrielle | Modelo treinado + API de inferência | M3 | Modelo com >85% mAP + latência <300ms |
| Gabrielle → Rafaela | Telas aprovadas + fluxo de coleta de métricas | M4 | 8 telas finalizadas + eventos trackados |
| Rafaela → Rayssa | Relatório de impacto do piloto | M6 | Linha de base + 3 indicadores primários |

---

## Tabela C — Cobertura Disciplinar (gap analysis)

Grade simples para evidenciar que o time cobre todas as disciplinas necessárias — ou, honestamente, para identificar onde é preciso uma contratação futura ou ICT parceira.

| Disciplina Necessária | Internalizada na Manacá? | Quem? | Lacuna → Estratégia |
|---|---|---|---|
| Visão computacional | ✅ | Alexandre + Gabriel | — |
| Arquitetura cloud | ✅ | Alexandre | — |
| Engenharia de dados de impacto | ✅ | Rafaela | — |
| UX/UI para IA | ✅ | Gabrielle | — |
| Articulação público-privada | ✅ | Rayssa | — |
| Metodologia de avaliação de impacto | ✅ | Ângelo + Rafaela | — |
| **Certificação laboratorial ISO/IEC 17025** | ❌ | — | Parceria com ICT {NOME} (rubrica Serviços de Terceiros) |
| **Ciência de Dados Pleno em redes neurais recorrentes** | ❌ | — | Contratação CLT M3 (rubrica Pessoal e Encargos) |

---

## Tabela D — Governança e Cadência de Alinhamento

| Ritual | Participantes | Frequência | Artefato |
|---|---|---|---|
| Daily técnica | CTO + Eng IA + PO | Diária, 15min | Log no Slack/Jira |
| Sprint review | Time todo + PR | Quinzenal, 1h | Ata + demo |
| Comitê de governança | Coordenador Geral + CTO + Diretora Metodológica | Mensal | Relatório de progresso + riscos |
| Reunião com {ICT parceira} | CTO + Coordenador ICT | Mensal | Ata + entrega de laudos |
| Reunião com {stakeholder} | CEO + representante | Bimensal | Ata de alinhamento |

---

## Como Transformar a Matriz em Redação (Fase 05b narrativa)

A matriz **não vai inteira** para a proposta (salvo se o edital pedir tabela). Ela é a **evidência** para uma redação como:

> "A governança do projeto foi desenhada para garantir máxima sinergia entre as frentes de Engenharia e Impacto. Alexandre Coleto (CTO, 40h/sem) lidera a arquitetura e o pipeline de visão computacional das Metas 1-2. Os modelos treinados alimentam diretamente a Meta 3, conduzida por Gabrielle Alves (Product Designer, 30h/sem), que transforma inferências técnicas em dashboards acionáveis para gestores públicos. Rafaela Rezende (Product Owner e Engenheira de Dados de Impacto, 40h/sem) fecha o ciclo na Meta 5, consolidando os indicadores de eficiência energética que constituem o critério E2.1 do edital. A cadência de alinhamento — daily técnica, sprint review quinzenal, comitê de governança mensal — é monitorada pela CEO Rayssa Mendes, que também articula a frente de parceria com a Prefeitura do Recife."

**Fórmula:** ordem cronológica das Metas → nome + papel + dedicação + entregável → como um alimenta o próximo → ritual de alinhamento → quem supervisiona.

---

## Checklist

- [ ] Toda meta do cronograma tem um responsável claro
- [ ] Toda disciplina necessária está coberta (ou tem estratégia de gap)
- [ ] Somatório de dedicações bate com o esforço das metas
- [ ] Handoffs têm critério de aceite definido
- [ ] Cadência de alinhamento é explícita (daily, sprint, mensal)
- [ ] Nenhuma pessoa aparece em metas conflitantes (sem sobrealocação)
