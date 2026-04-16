# Guia de Redação — Seção de Equipe em Editais

**Uso:** referência operacional do agente `edital-agent` nas fases 02, 03, 04, 05c, 06.
**Princípio:** a seção de equipe é o **documento fiduciário da inovação** — o avaliador está medindo risco de execução, não títulos. Cada linha deve mitigar uma incerteza.
**Premissa de flexibilidade:** este guia não se prende a um formato único (ex: Súmula FAPESP). A Manacá se inscreve em editais muito diferentes (agências de fomento, prêmios, editais corporativos, aceleradoras, editais internacionais). O agente deve **derivar o formato do edital específico** usando a matriz em `matriz-agencias-equipe.md` e os exemplos de tom em `templates/equipe/exemplos-redacao-equipe.md`.

---

## 1. O Tripé de Avaliação (universal, independe do edital)

Todo avaliador — seja de FAPESP, de prêmio corporativo ou de aceleradora — está avaliando o mesmo tripé:

### 1.1. Competência técnica comprovada

**O que o avaliador procura:** evidência concreta de que os nomeados dominam o estado da arte necessário para superar os gargalos do projeto.
**Como mostrar:** experiências anteriores **exatamente no tema** (não adjacentes), stack específico, portfólio de entregas, TRLs já alcançados em projetos prévios.
**O que evitar:** listas genéricas de "áreas de interesse"; CVs com currículo acadêmico total sem filtro.

### 1.2. Dedicação e dimensionamento

**O que o avaliador procura:** matemática que bate entre horas alocadas e escopo do cronograma.
**Como mostrar:** dedicação semanal explícita por pessoa + somatório compatível com as metas; PR / líder técnico com dedicação **substancial** (≥30h/semana quando o projeto é o foco da empresa).
**O que evitar:** dezenas de especialistas com 2h-4h semanais cada (aciona alerta de inexequibilidade); CEO acumulando tudo com 5h-10h.

### 1.3. Sinergia e complementaridade

**O que o avaliador procura:** como o trabalho de um alimenta o próximo na cadeia de P&D; governança clara.
**Como mostrar:** **matriz de competências × metas × TRL** (template: `matriz-competencias.md`); descrição explícita de handoffs; cadência de alinhamento.
**O que evitar:** amontoado de currículos desconexos deixando o avaliador juntar as peças.

---

## 2. Três Red Flags Fatais (mitigar ANTES de submeter)

### 2.1. "CEO Super-Homem" sem Dedicação

**Sintoma:** sócio único concentra Coordenador + Comercial + Técnico com 5-10h semanais.
**Percepção do avaliador:** o projeto é secundário; não vai acontecer.
**Correção:** atrelar a liderança técnica a um **CTO ou Pesquisador Executivo com ≥30h/semana**. O CEO cuida de institucional e comercial com horas condizentes.

### 2.2. Terceirização da Inteligência Central

**Sintoma:** empresa propõe arquitetura disruptiva mas manda 70% do orçamento para a universidade desenvolver o core.
**Percepção do avaliador:** empresa intermediária administrativa sem capacidade absortiva; PI em risco.
**Correção:** fomento contrata engenheiros internos (rubrica "Pessoal e Encargos"). A ICT atua **na periferia do risco** (laudos, testes, certificações) na rubrica "Serviços de Terceiros".

### 2.3. Desenquadramento Documental

**Sintoma:** Lattes desatualizado, ACT sem assinatura, Carta de Anuência faltando, link quebrado.
**Percepção do avaliador:** indeferimento automático em triagem preliminar — a banca de mérito nem chega a ler.
**Correção:** organizar documentação formal **em paralelo** à redação; revisão cruzada 2 dias antes da submissão; checklist de anexos na fase 07.

---

## 3. Compensação de Senioridade (quando não há PhDs)

A Manacá tem uma equipe enxuta com formação forte (USP, Columbia, UTFPR, Samsung, Petrobras) mas **sem doutorado**. Esse gap é superável se a narrativa compensar com:

- **Histórico documentado de entregas tecnológicas prévias** (MVPs lançados, pilotos em campo, contratos fechados).
- **Certificações técnicas de alto nível** (PMP, Lean, AWS, específicas).
- **Prêmios e reconhecimentos internacionais** (AI4GOOD Harvard/MIT, TDC SP).
- **Experiência em grande indústria** (Petrobras, Samsung, ArcelorMittal, Grupo Águia Branca).
- **Cultura "hacker + hustler"** explicitada: ciclos curtos de prototipagem, agilidade hands-on, validação com usuário final.

**Exemplo de redação (referência):**

> "A frente de Engenharia de Dados é liderada por [Alexandre Coleto], PMP e Engenheiro Eletricista pela Poli-USP, que arquitetou o pipeline SAIRA validado em TRL 4 em seis meses. A modelagem de negócios é conduzida por [Rayssa Mendes], cuja articulação fechou três PoCs no setor público alvo, incluindo o CPSI com a Prefeitura do Recife. Esta configuração operacional ágil (hands-on) permite ciclos contínuos de prototipagem, assegurando que o desenvolvimento ocorra sem distanciamento das demandas de mercado."

**Quando usar:** editais FINEP (StartUP, Centelha, Tecnova), BNDES, SEBRAEtec, aceleradoras — onde a agilidade de comercialização é compreendida como vetor de eficiência de capital.

**Quando NÃO usar:** editais acadêmicos puros (FAPESP PIPE, FACEPE doutorado) — aí a estratégia é outra: plugar uma ICT parceira com PR doutor em tema exato.

---

## 4. Matriz de Sinergia × Cronograma

**Princípio:** explicitar como o trabalho de cada pessoa **alimenta o próximo** na cadeia de P&D. O avaliador não deve precisar adivinhar a dinâmica do time.

**Estrutura:** template `matriz-competencias.md` (tabela Pessoa × Meta × Competência × TRL que atende).

**Exemplo de redação:**

> "A governança do projeto foi desenhada para garantir máxima sinergia. A Product Owner de Impacto [Rafaela] liderará o desenho de indicadores nas Metas 1-2 — as métricas geradas são o insumo direto para o Engenheiro de IA [Gabriel], que as codifica no modelo de scoring da Meta 3. A integração é monitorada semanalmente pelo CTO [Alexandre], assegurando alinhamento metodológico entre o frame de impacto e a stack técnica."

**Quando usar:** Trilha B (subvenção), editais de alta complexidade (FAPESP Fase 2, arranjos em rede FINEP/FACEPE). **Opcional na Trilha A** (prêmios) quando o limite de caracteres permitir.

---

## 5. Plano de Formação e Contratação Futura

**Princípio:** omitir a equipe futura é falha estrutural quando o projeto depende de contratações pagas pelo fomento.

**Estrutura (template `plano-contratacao-futura.md`):**

- Vaga (cargo, dedicação semanal, mês de contratação, rubrica "Pessoal e Encargos")
- Perfil profissiográfico (formação mínima, anos de experiência, competências)
- Impacto na meta específica
- Estratégia de recrutamento (parques tecnológicos, redes de alumni, comunidades tech, headhunters)

**Exemplo de redação:**

> "Para a Meta 4 (Otimização de Algoritmos Preditivos), o projeto aloca recursos para contratação, no mês 3, de um Cientista de Dados Pleno (40h/semanais). O perfil exige formação em Ciências da Computação ou Estatística, com mínimo 3 anos em redes neurais. O recrutamento será conduzido com apoio do TecVitória e da rede PMI-ES, mitigando risco de atraso."

**Quando usar:** Trilha B com orçamento substantivo (Subvenção FINEP, PIPE Fase 2, EMBRAPII). **Dispensável na Trilha A** (prêmios geralmente não pagam contratação).

---

## 6. ICTs e Parceiros Externos

**Princípio da periferia do risco:** a tecnologia central (core) **permanece interna**. ICTs atuam em:

- Certificações em ambiente simulado (TRL 5+)
- Ensaios destrutivos sob normas ISO
- Validações clínicas / laboratoriais
- Acesso a equipamentos multiusuários raros
- Laudos técnicos isentos

**Rubrica correta:** "Serviços de Terceiros" ou "Serviços de Consultoria" — **não** entram na aba "Equipe Executora" da FINEP.

**Limites orçamentários (consultar matriz por agência):**
- FAPESP PIPE Fase 1: máx 1/3 do valor para terceiros
- FAPESP PIPE Fase 2: máx 1/2
- FINEP arranjos em rede: mínimo 5% para ICT
- FACEPE Redes de Inovação: limites específicos por edital

**Documentação mandatória:**
- ACT (Acordo de Cooperação Técnica) chancelado
- Carta de Anuência institucional
- Carta de Anuência individual (por pesquisador envolvido)

**Exemplo de redação:**

> "O desenvolvimento do algoritmo permanece integralmente com a equipe da Manacá. Para a certificação em ambiente simulado (TRL 5), formalizamos parceria com [ICT X]. As atividades da ICT — vinculadas à rubrica 'Serviços de Consultoria' — limitam-se a ensaios sob norma [Y], garantindo validação isenta sem que a Manacá aliene o código-fonte ou o domínio da tecnologia central."

**Decisão da Manacá (2026-04):** não tratamos advisors formais com equity/vesting. Se um edital específico exigir, decidimos caso a caso.

---

## 7. Formato do CV / Súmula (decisão na Fase 04)

**Princípio:** não existe "formato padrão" universal. O agente escolhe a variante na Fase 04 (document-plan) usando a matriz `matriz-agencias-equipe.md`.

### Variantes disponíveis (detalhes em `templates/equipe/sumula-curricular.md`):

| Variante | Quando usar | Tamanho | Tom |
|---|---|---|---|
| **Súmula FAPESP** | FAPESP PIPE/TC/PITE | 2 páginas estritas | Acadêmico-científico |
| **Currículo livre FINEP** | FINEP (FAP), Tecnova, Centelha, StartUP | 1-2 páginas | Industrial + tração |
| **Currículo EMBRAPII** | EMBRAPII, chamadas de encomenda | Padrão industrial | P&D aplicado |
| **Lattes atualizado** | FAPs estaduais (FACEPE, FAPESB, FAPERJ, FAPES) | Link + resumo de 1 página | Acadêmico |
| **Mini-bio de prêmio** | Prêmios (CSC, Josué Castro, Mulheres Inovadoras, Shell, Sebrae) | 1 parágrafo por pessoa ou 1 linha | Punchy, hook, tração |
| **Formato corporativo** | Editais corporativos (Shell, Reckitt, Unilever, BNDES Garagem) | 1 página por pessoa | Executivo, foco em resultados de negócio |
| **Formato internacional** | IDB, Google.org, AI4GOOD, editais EU/US | 1-2 páginas em inglês | Impact-driven, métricas mensuráveis |

### Regras universais (todas as variantes):

- Cabeçalho com **cargo no projeto + dedicação semanal** (quando aplicável) + links válidos.
- Omitir estado civil, dados pessoais irrelevantes.
- Substituir "Lista de Publicações" por **Resultados de Inovação** (patentes, software INPI, MVPs, contratos, prêmios) quando o edital não for puramente acadêmico.
- Destacar experiência de **gestão de projetos financiados** previamente (mostra compreensão da responsabilidade legal).
- Incluir **rede de relacionamento** quando relevante (alumni, associações, programas).

---

## 8. Fluxo de Reescrita Customizada (nova sub-fase 05c)

Quando o agente chega na seção de equipe de um edital novo:

### 05c.1 — Team Fit Analysis

1. Lê `01-edital-parsed.md` (critérios de avaliação, peso da equipe, agência).
2. Lê `03-project-suggestion.md` (projeto proposto, metas, TRL).
3. Lê `matriz-agencias-equipe.md` (regras específicas da agência).
4. **Imagina a "equipe perfeita"** para vencer aquele edital:
   - Papéis necessários (PR, CTO, pesquisadores, consultores, ICT)
   - Perfil ideal de cada papel (formação, experiência, competências)
   - Dedicação esperada por papel
5. Mapeia a equipe real da Manacá (via `Equipe/CVs-Canonicos/`) contra a equipe ideal.
6. Identifica **gaps** e decide estratégia: redação compensatória, contratação futura, ICT parceira, ou — em último caso — no-go.

Output: `editais/<slug>/05c1-team-fit.md`.

### 05c.2 — CV Rewrite

Para cada pessoa:
1. Abre o CV canônico (`Equipe/CVs-Canonicos/<nome>.md`).
2. Usa as **"Notas Estratégicas para Reescrita"** no final de cada arquivo canônico como norte.
3. Seleciona/prioriza/reformula as experiências que **mais aproximam o perfil real do perfil ideal**.
4. Aplica a variante de formato escolhida na Fase 04.
5. Escreve o CV final em `editais/<slug>/05c2-cvs-customizados/<nome>.md`.

**Regra inviolável:** não inventar nada. Só iluminar, reordenar, traduzir para a linguagem da banca.

---

## 9. Checklist de Qualidade (rodar na Fase 06)

Oito perguntas — cada "não" é bloqueador até mitigação:

1. **Integridade da Liderança:** há um único Coordenador/PR designado com aderência irrefutável ao tema?
2. **Coerência de Dedicação:** somatório de horas bate com o cronograma físico? Não há dedicações simbólicas?
3. **Vínculos Fiscais:** sócios estão separados de funcionários CLT e terceiros? Respeita regras da agência sobre pró-labore?
4. **Blindagem do Core:** argumentação deixa explícito que engenharia central e código-fonte ficam internos?
5. **Sanidade Documental:** links Lattes/LinkedIn funcionam? CVs respeitam limite de páginas?
6. **Avaliação Jurídica de Terceiros:** todo parceiro ICT tem ACT + Carta de Anuência anexados?
7. **Rastreabilidade da Sinergia:** governança e cadência de alinhamento estão descritas?
8. **Reescrita Sob Medida:** cada CV destaca o que o edital mais valoriza? Tom correto para a banca (acadêmica/industrial/corporativa/internacional)?

---

## 10. Referências

- `pesquisas/equipe-editais-boas-praticas.md` — pesquisa completa (fonte original)
- `matriz-agencias-equipe.md` — regras por agência com gatilhos de red-flag
- `templates/equipe/` — 5 templates operacionais
- `Editais/Equipe/CVs-Canonicos/` — matéria-prima dos CVs
