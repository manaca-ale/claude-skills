---
type: guide
canonical_for: []
derived_from: []
---

# Guia de Redação para Propostas de Editais de Inovação

> **NOTA (2026-04-26):** este guia tem ~230 palavras sem acentuação completa do legacy (foi escrito antes da regra de "acentuação desde primeiro rascunho"). O conteúdo é válido — está pendente de uma passada de cleanup textual. **Mais importante:** ao escrever propostas novas, siga a regra do `SKILL.md > Princípios de Escrita PT-BR` (acentuação completa desde o primeiro draft, nunca pós-corrigir). O título, os cabeçalhos e a tabela abaixo já foram corrigidos como exemplo.

Referência prática para o agente de redação. Consulte este documento ao redigir qualquer seção de proposta para editais FINEP, FAPESP, EMBRAPII, FAPs estaduais e programas correlatos.

---

## 1. Estrutura da Narrativa

Toda proposta segue um arco argumentativo único. Cada seção deve alimentar a próxima de forma causal.

**Fluxo obrigatório:**

Problema (quantificado) → Estado da Arte (lacuna técnica) → Solução Proposta (inovação) → Metodologia de P&D → Equipe e Capacidade → Viabilidade Econômica e Impacto

### Regras por seção

| Seção | Objetivo | Deve conter |
|---|---|---|
| Problema | Convencer que a dor é real e mensurável | Dados de institutos (IBGE, IPEA, MAPA), cifras de perda, número de afetados |
| Estado da Arte | Provar que soluções existentes falham | Mapeamento de concorrentes diretos e indiretos, limitações técnicas específicas |
| Solução | Descrever a inovação e o risco tecnológico | Arquitetura técnica, algoritmos, diferencial frente ao estado da arte |
| Metodologia | Detalhar como o risco será superado | Frameworks, modelos matemáticos, datasets, testes planejados, métricas de sucesso |
| Equipe | Demonstrar capacidade de execução | Currículos narrativos, tríade ciência+mercado+gestão |
| Viabilidade | Provar ida ao mercado | TAM/SAM/SOM, modelo de receita, cartas de intenção, early adopters |

### Anti-padroes

- NUNCA afirme inovacao sem demonstrar. Sistema revolucionario e marketing, nao ciencia.
- NUNCA omita concorrentes. O avaliador conhece o mercado; omitir Salesforce, Dynamics ou similares quando relevantes destroi credibilidade.
- NUNCA confunda impacto social com inovacao tecnologica. O fato de o software ajudar ONGs nao configura risco tecnico.
---

## 2. Tom e Registro

### Principios inegociaveis

- **Formal e assertivo.** Voz ativa, frases diretas.
- **Imparcial e ancorado em dados.** Cada afirmacao quantitativa deve ter fonte.
- **Sem adjetivos hiperbolicos.** Proibidos: revolucionario, inedito, unico, perfeito, disruptivo (a menos que demonstrado tecnicamente).
- **Equilibrio entre profundidade tecnica e acessibilidade.** Secoes de metodologia usam terminologia de engenharia de software e ciencia da computacao. Resumo executivo e impacto social devem ser compreensiveis para avaliador de administracao ou ciencias sociais.

### Construcoes preferidas

| Evitar | Preferir |
|---|---|
| O sistema e o mais avancado do mercado | A arquitetura proposta supera as limitacoes de X ao implementar Y, conforme demonstrado na Secao 3.2 |
| Nao existe nada parecido | A analise do estado da arte (Tabela 1) evidencia que as solucoes disponiveis nao atendem ao requisito Z por limitacao W |
| Enorme impacto social | A projecao SROI indica retorno de R$ 3,80 para cada R$ 1,00 investido (metodologia detalhada no Anexo B) |

### Formatacao para escaneabilidade

- Use **negrito** para KPIs, metodologias e milestones.
- Quebre paragrafos longos. Maximo de 5-6 linhas por paragrafo.
- Use tabelas comparativas para estado da arte e orcamento.
- Use listas numeradas para sequencias logicas (etapas, WPs).

---

## 3. Distribuicao de Espaco

Proporcao recomendada para o corpo tecnico da proposta:

| Bloco | % do espaco | Conteudo prioritario |
|---|---|---|
| Problema + Estado da Arte | 15% | Quantificacao, lacuna tecnica, concorrentes |
| Metodologia + Superacao do risco tecnologico | 40% | Arquitetura, algoritmos, frameworks, testes, metricas |
| Mercado + Impacto ESG/ODS | 25% | TAM/SAM/SOM, modelo de negocio, SROI, Teoria da Mudanca |
| Cronograma + Equipe + Orcamento | 20% | WPs, Gantt, curriculos narrativos, justificativa SMART |

Se a plataforma de submissao impoe limites de caracteres por campo, redistribua proporcionalmente mantendo a prioridade da metodologia.
---

## 4. TRL (Technology Readiness Level)

Ao descrever o TRL, SEMPRE declare: (a) TRL atual com evidencias, (b) TRL alvo ao final do projeto.

### TRL 4 - Validacao de Componentes em Laboratorio

**O que demonstrar:** Algoritmos codificados e testados isoladamente com dados sinteticos.

**Evidencias para SaaS:** Jupyter Notebooks com modelos matematicos; testes unitarios em back-end local; relatorios de accuracy em datasets sinteticos; repositorio de codigo versionado.

**Exemplo de redacao:** O projeto encontra-se no TRL 4. Os modelos de inferencia preditiva foram codificados em Python e integrados a uma estrutura de back-end local. A validacao funcional utilizou datasets sinteticos simulando o comportamento-alvo. Os testes demonstraram capacidade de identificar padroes primarios, sem processamento em tempo real ou GUI consolidada.

### TRL 5 - Validacao em Ambiente Relevante

**O que demonstrar:** Software operando em infra que simula nuvem comercial, com dados reais (ainda que estaticos).

**Evidencias para SaaS:** Deploy em ambiente de homologacao (AWS/GCP/Azure); testes com base anonimizada de dados reais de parceiro; integracao via sandbox com APIs externas; relatorios de performance.

### TRL 6 - Prototipo/MVP em Ambiente Relevante (Beta)

**O que demonstrar:** MVP integrado, hospedado em nuvem de producao, usado por usuarios reais em piloto.

**Evidencias para SaaS:** Programa Closed Beta documentado com duracao, numero de organizacoes, metricas de latencia, uptime, consumo de recursos; relatorios de correcao de gargalos; termos assinados por beta-testers.

### TRL 7 - Prototipo em Ambiente Operacional (Early Adopters)

**O que demonstrar:** Sistema operando autonomamente em ambiente real de clientes, sem intervencao direta de desenvolvedores.

**Evidencias para SaaS:** Base de early adopters pagantes; integracao completa com fluxos de trabalho reais; certificacao de seguranca preliminar; metricas de uso diario.

### Erros fatais de TRL

- Superestimar (TRL 8-9) para impressionar: banca nega fomento pois risco tecnologico superado.
- Subestimar (TRL 1-2) para parecer ambicioso: banca classifica como pesquisa basica distante do mercado.
- Afirmar TRL sem evidencias documentais.

---

## 5. Justificativa Orcamentaria

### Metodo SMART para cada rubrica

Cada item do orcamento deve responder:

1. **S (Specific):** O que sera contratado/adquirido, com especificacao tecnica.
2. **M (Measurable):** Quantidade, horas, volume mensuravel.
3. **A (Achievable):** Baseado em media de 3 cotacoes reais.
4. **R (Relevant):** Vinculado a qual Meta de qual Work Package.
5. **T (Time-bound):** Em qual periodo do cronograma sera executado.

### Estrutura da justificativa

[Rubrica]: [Valor] - Vinculada a Meta X do WP Y.
Justificativa tecnica: [Por que este item e indispensavel para superar o risco tecnologico].
Base de calculo: [Detalhamento de quantidade x valor unitario, com referencia a cotacoes].

### Gatilhos comuns de glosa (evitar)

- Terceirizar o core do desenvolvimento (anula o proposito da subvencao a MPE).
- Prever equipamentos permanentes em editais exclusivos de custeio.
- Orcamento com valores redondos sem base em cotacoes reais.
- Solicitar exatamente o teto maximo sem justificativa granular.
- Incluir marketing comercial, aluguel nao vinculado, pro-labore quando vedado.
- Prever hospedagem comercial com recursos de P&D (separar GPU de treinamento vs. hosting producao).

### Contrapartidas

- **Financeira:** Aporte em dinheiro na conta do projeto. Comprovar com balanco patrimonial.
- **Economica:** Infraestrutura propria, licencas preexistentes, horas de equipe (valoradas a preco de mercado).
- EMBRAPII usa regra do 1/3: empresa 1/3, EMBRAPII 1/3, ICT 1/3.
---

## 6. Propriedade Intelectual

### Dois modelos aceitos para parcerias com ICT/IES

**Modelo 1 - Cotitularidade Proporcional:**
- Empresa e ICT compartilham propriedade do codigo/algoritmo.
- Empresa recebe exclusividade de exploracao comercial.
- ICT recebe royalties (% sobre receita liquida) apos comercializacao.
- Redacao deve prever: percentuais de titularidade, prazo de exclusividade, calendario de royalties.

**Modelo 2 - Cessao Total a Empresa com Clausula de Reversao:**
- ICT cede 100% dos direitos de PI a empresa (art. 37, Decreto 9.283/18).
- Clausula de reversao obrigatoria: se empresa nao comercializar em 24-36 meses, PI retorna a ICT.
- Demonstra amadurecimento juridico e compromisso de ida ao mercado.

### Requisitos documentais

- Acordo de Parceria ou Termo de Sigilo pre-aprovado pelo NIT da ICT.
- Minutas baseadas nos modelos PGF/AGU.
- Para SaaS: Registro de Programa de Computador (INPI) + manutencao de Segredo Industrial sobre algoritmos proprietarios.
- Custos de registro sao da empresa, nao financiaveis por subvencao.

---

## 7. Impacto Social e ESG

### Framework: Teoria da Mudanca (Theory of Change)

Toda narrativa de impacto deve seguir a cadeia causal completa:

Insumos (tecnologia + fomento) --> Atividades (processamento, inferencia, integracao) --> Produtos/Outputs (dashboard, relatorios automatizados) --> Resultados/Outcomes (economia de X horas, reducao de CAC em Y%) --> Impacto de Longo Prazo (ampliacao de Z% no atendimento assistencial)

### SROI (Social Return on Investment)

Incluir projecao formal: Para cada R$ 1,00 investido, a plataforma gera R$ X,XX em valor social monetizado.

A monetizacao deve derivar de metricas auditaveis: horas-homem economizadas (valoradas por salario medio do setor), perdas financeiras evitadas, custos de conformidade reduzidos.

### Alinhamento ODS

- NUNCA cite ODS genericamente (alinhado ao ODS 10).
- SEMPRE cite a sub-meta especifica: ODS 16, sub-meta 16.6: desenvolver instituicoes eficazes, responsaveis e transparentes.
- Conecte a funcionalidade tecnica a sub-meta: qual modulo do sistema atende qual sub-meta e como.

---

## 8. Competencia da Equipe

### Triade obrigatoria

| Pilar | Perfil | O que demonstrar |
|---|---|---|
| Cientifico | CTO / Pesquisador Responsavel | Mestrado/Doutorado, papers, patentes, experiencia com incerteza tecnologica |
| Mercado | CEO / Gestor de Negocios | Historico de gestao comercial, fundraising, vivencia no setor-alvo |
| Gestao | Scrum Master / Compliance | Capacidade de entrega continua, gestao de metas sob escrutinio governamental |

### Curriculo narrativo (nao Lattes bruto)

Cada membro deve ter um paragrafo de 3-5 linhas que:
1. Conecte a formacao ao desafio especifico do projeto.
2. Cite realizacoes quantificaveis anteriores (N patentes, N projetos entregues, N anos de experiencia).
3. Informe a dedicacao em horas/semana ao projeto.

**Exemplo:** A coordenacao cientifica sera conduzida por [Nome], Doutor em Ciencia da Computacao (Lattes: link), com 10 anos de experiencia em sistemas distribuidos e autor de 4 patentes em Machine Learning. Dedicacao: 20h/semana nas fases WP1-WP3.

### Erros a evitar

- Pesquisadores brilhantes cuja especialidade nao tem relacao com o projeto.
- Equipe 100% tecnica sem cerebro comercial (sinaliza risco de falha na comercializacao).
- Curriculos sem link para Lattes ou ORCID.
---

## 9. Cronogramas

### Estrutura de Work Packages

| WP | Periodo tipico (24 meses) | Foco | Entregavel comprobatorio |
|---|---|---|---|
| WP1 | Meses 1-4 | Modelagem, requisitos, arquitetura de dados | Relatorio de Especificacao Arquitetural; Termo de Adesao LGPD |
| WP2 | Meses 4-10 | Prova de conceito, treinamento de IA (TRL 4) | Relatorio Tecnico com taxas de accuracy; testes de regressao |
| WP3 | Meses 10-16 | Integracao, piloto minimo (TRL 5-6) | Certificado Pentest; registros de disponibilidade do servidor |
| WP4 | Meses 16-24 | Ambiente real (TRL 7), comercializacao preliminar | Deposito INPI; Termos de Recebimento assinados por beta-testers |

### Regras de cronograma

- Cada liberacao de recurso deve estar vinculada a verificacao do entregavel do WP correspondente.
- Incluir **buffer temporal** entre WPs (minimo 2-4 semanas). Cronograma sem folga e risco de cronograma inviavel.
- Descrever explicitamente o **plano de mitigacao** para desvios cronologicos.
- Usar Gantt com caminho critico e responsaveis claros por etapa.
- Cada entregavel deve ter um documento de comprovacao descrito (se o avaliador nao sabe como o Governo verificara a conclusao, reduz a pontuacao).

### Anti-padrao

- Tarefas de alta complexidade em janelas de 1 mes.
- Dependencias em cascata sem slack time (atraso em WP2 trava financeiramente WP3).

---

## 10. Checklist de Due Diligence Pre-Submissao

- [ ] **CNDs:** Todas as Certidoes Negativas de Debito (Federal, Estadual, Municipal, Trabalhista, FGTS) vigentes na janela de submissao E contratacao. Validar com 30 dias de antecedencia.
- [ ] **Enquadramento:** CNPJ possui idade minima exigida? Porte (ME/EPP/LTDA/S.A.) conforme edital? Nenhum socio ou bolsista com inadimplencia em projetos anteriores?
- [ ] **Rubricas:** Nenhum item viola as proibicoes do edital (bens de capital em edital de custeio, pro-labore vedado, etc.)?
- [ ] **TRL:** Transicao TRL atual -> TRL alvo esta coesa, com metricas empiricas e evidencias documentais?
- [ ] **Risco tecnologico:** O texto demonstra incerteza cientifica (ML, NLP, algoritmos ineditos), nao mero esforco de engenharia de software tradicional?
- [ ] **Propriedade intelectual:** Acordo com NIT pre-negociado e assinado? Modelo de partilha (cotitularidade ou cessao com reversao) descrito no corpo da proposta?
- [ ] **Impacto ESG/ODS:** Teoria da Mudanca completa (Insumos -> Impacto)? SROI projetado? ODS com sub-meta especifica?
- [ ] **Contrapartida:** Capacidade financeira demonstravel pelo balanco patrimonial?
- [ ] **Matriz de avaliacao:** Pesos do edital mapeados e esforco de redacao distribuido proporcionalmente?
- [ ] **Formatacao:** Valores em formato brasileiro, datas por extenso, sem erros de portugues?
---

## 11. Erros Fatais a Evitar

### Eliminacao administrativa (binaria)

1. Inadimplencia de qualquer participante em projetos anteriores.
2. Desenquadramento de porte (MEI em edital que exige LTDA/S.A.).
3. Itens nao financiaveis no orcamento (bens de capital, marketing, aluguel vedado).
4. CNDs vencidas no momento da submissao ou contratacao.
5. Coordenador com vinculo CLT exclusivo incompativel (PIPE FAPESP).

### Baixa pontuacao de merito

1. Ausencia de risco tecnologico demonstravel (confundir com risco de mercado).
2. Miopia mercadologica: foco exclusivo em beleza tecnica sem plano de comercializacao.
3. TRL incompativel com o instrumento de fomento.
4. Impacto social baseado em achismo sem metodologia (SROI, ToC).
5. Equipe desalinhada com os desafios tecnicos do projeto.
6. Orcamento sem vinculacao 1:1 com Work Packages.
7. Cronograma sem entregaveis verificaveis.
8. Paragrafos densos sem formatacao, dificultando leitura transversal.
9. Omissao de concorrentes na analise do estado da arte.
10. Declarar inovacao por adjetivos em vez de demonstrar por especificacoes tecnicas.

---

## 12. Padroes de Formatacao

### Valores monetarios

- Formato: R$ 1.000.000,00 (ponto como separador de milhar, virgula para decimais).
- Sempre com duas casas decimais.
- Valores no orcamento devem ser quebrados (baseados em calculo real), nao arredondados.

### Datas

- Formato por extenso: 14 de abril de 2025.
- Em tabelas e cronogramas, aceito: abr/2025 ou 04/2025.

### Construcoes formais

| Evitar | Usar |
|---|---|
| a gente vai fazer | a equipe executara |
| esse sistema | a plataforma proposta / o sistema objeto deste projeto |
| basicamente | (suprimir) |
| muito importante | determinante para / indispensavel a |
| hoje em dia | no cenario atual / no contexto vigente |
| vamos provar que funciona | a validacao sera conduzida mediante [metodologia] |

### Siglas

- Na primeira ocorrencia: nome completo seguido da sigla entre parenteses.
- Exemplo: Organizacoes da Sociedade Civil (OSCs).
- A partir da segunda ocorrencia: apenas a sigla.

### Referencias e fontes

- Dados quantitativos devem citar a fonte entre parenteses: (IBGE, 2024) ou (Relatorio FINEP, 2025).
- Preferir fontes oficiais: IBGE, IPEA, MCTI, Banco Mundial, ONU.

---

## Referencia Rapida: Pesos Tipicos de Avaliacao

| Dimensao | Peso tipico | Prioridade na redacao |
|---|---|---|
| Merito Tecnologico / Grau de Inovacao | Altissimo (eliminatorio) | Maxima |
| Consistencia da Metodologia Cientifica | Alto | Alta |
| Viabilidade Economica / Comercializacao | Medio-Alto | Alta |
| Impacto Socioambiental / ESG / ODS | Alto (tendencia 2023-2026) | Alta |
| Capacidade da Equipe | Medio | Media |
| Adequacao Orcamentaria / Cronograma | Eliminatorio se inconsistente | Alta |

**Regra de ouro:** Antes de submeter, localize no edital a tabela de pesos e redistribua o esforco de redacao e contagem de caracteres proporcionalmente.

---

## 13. Exemplos Canônicos — Inscrições Submetidas pela Rayssa (abr/2026)

Esta seção compila trechos retirados de 3 inscrições reais da Manacá em editais relevantes (PES 2026, WOW Aceleradora Batch #34, Prêmio Sebrae Startups 2026). São padrões de redação que **funcionaram** em formulários de prêmios e aceleração em pt-BR. Use como base estilística e estrutural quando precisar redigir campos análogos.

> **Localização das fontes originais:** `c:\Editais\01. Submetidos\` (subpastas com regulamento, respostas e link do Drive).

### 13.1 Perfil curto do empreendedor (PES 2026 Q17)

**Quando usar:** campos de "perfil/biografia executiva" em prêmios de empreendedorismo, formulários de aceleração, sites institucionais.

**Estrutura:** formação acadêmica → trajetória de impacto → projetos liderados na Manacá → reconhecimentos → links sociais.

**Exemplo (Rayssa Mendes):**

> Rayssa Pereira do Nascimento Mendes é cientista social, historiadora e empreendedora dedicada a democratizar o uso de dados para a transformação socioambiental. Com bacharelado e mestrado em Ciências Sociais (PUC-SP), graduação em História (USP) e MBA em Gestão de Projetos (USP/Esalq), acumula mais de uma década de experiência em pesquisa e avaliação de impacto junto a instituições como UNICEF, Banco Mundial, Fundação Lemann e Itaú Social.
>
> Sua trajetória é marcada pela vivência na ponta, tendo atuado como professora em escolas públicas pelo programa Ensina Brasil e na gestão pública pela Secretaria de Cultura do Espírito Santo, via programa da Vetor/Motriz Brasil. Essas experiências revelaram um gargalo crítico: a dificuldade de organizações e governos em mensurar e comprovar resultados reais, o que motivou a fundação da Manacá Tecnologias Sociais em 2022.
>
> À frente da Manacá, Rayssa lidera o desenvolvimento de soluções tecnológicas inovadoras, como a Flora (SaaS) e o Saíra (CPSI Recife). Sob sua liderança, a Manacá recebeu o Selo de Negócio Sustentável da Shell Iniciativa Jovem e foi premiada no AI4GOOD da Brazil Conference (Harvard & MIT) pelo projeto ResiliêncIA.

### 13.2 Descrição do desafio + solução inovadora (PES 2026 Q23)

**Quando usar:** campos de "qual problema sua iniciativa resolve" / "qual a inovação proposta".

**Estrutura:** contexto quantificado → metodologia diferencial → produto âncora → laboratório PD&I.

**Exemplo:**

> O Brasil possui milhares de organizações, fundos e governos gerando impacto, mas a maioria esbarra em um gargalo crítico: a falta de inteligência, tecnologia e governança de dados para comprovar resultados. Sem estruturar evidências claras, perde-se financiamento e formulam-se políticas ineficientes para desafios urgentes, como as mudanças climáticas e a gestão de resíduos sólidos.
>
> A Manacá resolve essa dor atuando na interseção entre inovação tecnológica e transformação socioambiental. Nossa abordagem inovadora está na metodologia: nós traduzimos o rigor científico e a complexidade estatística para soluções de dados acessíveis e escaláveis. Diferente de consultorias genéricas, entregamos inteligência de impacto contínua, unindo metodologias consagradas (como a Teoria de Mudança) à Engenharia de Software e IA.
>
> Para dar escala a essa metodologia, desenvolvemos a Flora, nossa plataforma central (SaaS). Além disso, a Manacá atua como um laboratório de inovações contínuas (PD&I) para resolver complexidades territoriais. Desse braço nascem tecnologias específicas, como o Saíra, o ResiliêncIA e o BT Tracker.

### 13.3 Atuação e projetos em andamento (PES 2026 Q24)

**Quando usar:** campos de "como sua iniciativa atua" ou "projetos em andamento".

**Estrutura:** eixos numerados → clientes citados linha-a-linha com 1 frase de contexto.

**Exemplo:**

> 1. **Plataforma Flora e Gestão de Impacto (SaaS e Consultoria Estratégica)**: nossa principal frente. Centraliza modelos lógicos, biblioteca de evidências, dashboards interativos e relatórios automatizados.
>    - Bbutton: aceleradora de negócios, cliente recorrente que potencializa o crescimento de seu portfólio.
>    - Bracell: estudo de impacto do portfólio de Investimento Social Privado.
>    - Ensina Brasil: gestão logística e análise de indicadores recorrente desde 2022, impactando mais de 41 mil estudantes.
>    - Fundo Vale e Pipe Social: estudo de impacto com 114 negócios apoiados.
>    - Arco Instituto e Instituto Aprender Cultura: estruturação de Teoria da Mudança.
>
> 2. **Tecnologias Territoriais e Inovação Aberta (Saíra e PD&I)**: soluções para cidades sustentáveis.
>    - Saíra (Recife): Contrato Público de Solução Inovadora (CPSI) com a Prefeitura. MVP cobrirá até 10 pontos críticos com câmeras inteligentes e visão computacional.
>    - PD&I: ResiliêncIA e BT Tracker, ambos premiados no AI4GOOD da Brazil Conference.

### 13.4 Resultados quantificados (PES 2026 Q25)

**Quando usar:** campo de "principais resultados" em prêmios e aceleradoras.

**Estrutura hierárquica obrigatória:** ALCANCE E ESCALA → IMPACTO QUANTIFICADO → CRESCIMENTO FINANCEIRO → CAPTAÇÃO VIA EDITAIS → RECONHECIMENTOS → ACELERAÇÕES.

**Exemplo:**

> ALCANCE E ESCALA
> - 14 municípios atendidos em 11 estados e 3 regiões: Vitória/ES, Cariacica/ES, São Paulo/SP, Rio de Janeiro/RJ, Belo Horizonte/MG, Alagoinhas/BA, Caruaru/PE, Caucaia/CE, São Luís/MA, Campo Grande/MS, Cuiabá/MT, Águas Lindas de GO, Luziânia/GO, Aparecida de Goiânia/GO
> - 14 clientes pagantes, 19 projetos entregues, 5 workshops/formações
> - Primeiros clientes SaaS na plataforma Flora
> - 2 sócios + 4 colaboradores fixos, equipe fixa majoritariamente feminina (67%, incl. CEO)
>
> IMPACTO QUANTIFICADO
> - 23 redes de ensino impactadas
> - 41.406 estudantes impactados
> - 839 professores impactados
> - 261 gestores impactados
> - 114 negócios de impacto pesquisados
> - 5 Teorias de Mudança elaboradas/revisadas
>
> CRESCIMENTO FINANCEIRO (valores submetidos InovAtiva mai/2026)
> - Faturamento: R$ 34.176 (2022) → R$ 94.093 (2023) → R$ 225.950 (2024) → R$ 125.630 (2025) → R$ 198.677 (2026 até mai)
> - Faturamento últimos 12 meses: R$ 259.846,27
> - Faturamento total acumulado (desde 2022): ~R$ 678 mil
> - CAGR: ~75% a.a.
>
> CAPTAÇÃO NÃO-DILUTIVA (~R$ 358 mil — submetido InovAtiva)
> - Subvenção estrita: R$ 255.600 (Centelha+NIS 2023 R$130k; Seedes 2025 R$100k; Empreendedoras Tech 2025 R$26k)
> - Bolsas: Centelha R$26k, Empreendedoras Tech R$26k
> - Premiações: Shell R$5k (2025); Prêmio Mudar/Ensina Brasil R$20k (2025)
> - Aprovações 2026: Vai Tec/ADE Sampa R$52k
>
> RECONHECIMENTOS
> - Selo "Projeto com Propósito" — PMI-ES (2026)
> - Prêmio de Impacto Social AI4GOOD — Brazil Conference at Harvard/MIT (2025)
> - Selo de Negócio Sustentável — Shell (2025)
> - Seleção Portal Impacta Brasil — MDIC, celeiro de soluções da COP30 (2025)
>
> ACELERAÇÕES
> - Potência UP (Artemisia), Seedes (Neo Ventures), Empreendedoras Tech (Sebrae/MDIC), Centelha ES (FAPES, 2023)
> - Shell Iniciativa Jovem (2024), RME Acelera (2023), Future Females (2021)
> - Inovativa de Impacto (2022), Startup Lab USP (2020)

### 13.5 Capacidade executora (Sebrae Startups Q5)

**Quando usar:** campo "como o time de fundadores foi formado" / "capacidade executora".

**Estrutura:** sinergia entre formações + papel de cada sócio + complementaridade.

**Exemplo:**

> A Manacá nasceu para unir o rigor do impacto socioambiental à escalabilidade da tecnologia de ponta. Formamos um time multidisciplinar de alta densidade técnica, focado em transformar dados complexos em decisões estratégicas.
>
> A liderança é exercida pela CEO Rayssa Mendes (cientista social PUC-SP/USP), que aporta sua sólida experiência em avaliação de impacto junto a organismos de referência, como UNICEF, Banco Mundial e Fundação Lemann, garantindo precisão metodológica.
>
> A frente tecnológica é liderada pelo CTO Alexandre Coleto (engenheiro Poli-USP e PMP), especialista em arquitetura de software, automação SaaS e gestão de projetos complexos.
>
> O time de execução conta ainda com especialistas em Operações (Rafaela Reis), focada em eficiência de processos e indicadores, e Produto/UX (Gabrielle Alves), que assegura a usabilidade e a entrega de valor centrada no usuário.
>
> Essa sinergia entre Ciências Sociais, Engenharia e Design permite que a Manacá entregue soluções robustas e escaláveis, consolidando uma capacidade executora diferenciada no setor de impacto.

### 13.6 Vantagem competitiva (Sebrae Startups Q6)

**Estrutura:** três frentes de concorrentes (consultoria + plataformas + IA genérica) → 5 diferenciais Manacá numerados.

**Exemplo:**

> Nosso cenário competitivo divide-se em três frentes: consultorias tradicionais (ex: Move Social), que oferecem rigor mas são lentas e de alto custo; plataformas de gestão (Bússola Social, Sopact), que organizam dados mas exigem expertise analítica do cliente; e IA genérica (ChatGPT), que carece de segurança de dados e método científico.
>
> Nossa vantagem competitiva reside em unir o melhor desses mundos: entregamos a precisão metodológica das grandes consultorias por meio de uma plataforma SaaS automatizada.
>
> Nossos principais diferenciais são:
> 1. **IA Explicável (XAI):** A Flora não apenas armazena dados, mas interpreta e gera relatórios confiáveis e auditáveis automaticamente.
> 2. **Aderência local + LGPD:** Integração nativa com bases públicas brasileiras (IBGE, AdaptaBrasil) e total segurança e privacidade de dados.
> 3. **Custo-benefício:** Democratizamos a inteligência de impacto com uma operação até 80% mais acessível que os modelos tradicionais.
> 4. **Abordagem 360°:** Estratégia + dados + impacto, vs. soluções fragmentadas.
> 5. **Validação enterprise:** Suzano, Bracell, Prefeitura do Recife (CPSI).

### 13.7 Maior desafio e como superou (PES 2026 Q27)

**Estrutura:** narrativa em primeira pessoa, com 3 frentes de superação numeradas.

**Exemplo:**

> O maior desafio à frente da Manacá foi me consolidar como fundadora — mulher, cientista social e empreendedora de primeira viagem — sem capital inicial e em um mercado nacional que não é orientado a dados e pouco valoriza impacto socioambiental.
>
> Operamos em bootstrapping entre 2022 e 2023. Com faturamento inicial de apenas R$ 34 mil, o dilema era financiar a operação e a tecnologia simultaneamente. A saída estratégica foi equilibrar a venda de consultorias (geração de caixa) com o desenvolvimento da plataforma Flora (visão de longo prazo).
>
> O avanço para o Saíra exigiu incorporar IA e visão computacional, áreas fora da minha formação. Contornei isso usando o vesting: estruturei um modelo societário atrativo para atrair talentos e especialistas de ponta engajados pelo propósito. Para romper a barreira de entrada no setor público (B2G), utilizamos o Contrato Público de Solução Inovadora (CPSI) e o Marco Legal das Startups, inserindo nossa tecnologia estrategicamente via desafios de inovação aberta.
>
> Para superar esses obstáculos, atuei em três frentes:
> 1. **Validação estratégica:** busca ativa por grandes acelerações e editais de inovação, visando capital não-diluível, parcerias e chancela institucional.
> 2. **Casos de Sucesso:** foco em gerar resultados rápidos para os primeiros clientes, consolidando a prova de conceito.
> 3. **Formação contínua:** imersão em cursos e capacitações para fortalecer minha visão de negócios.

### 13.8 Por que mereço o prêmio (PES 2026 Q29)

**Estrutura:** 3 parágrafos curtos — missão → tração → diferencial.

**Exemplo:**

> Mereço este reconhecimento porque decidi dar voz e visibilidade a quem transforma o Brasil. Hoje, iniciativas brilhantes morrem por não conseguirem provar o seu valor. A Manacá nasceu para ser essa ponte: unimos o trabalho de quem gera impacto real, no chão das comunidades, à tecnologia que destrava financiamentos e escala políticas públicas.
>
> Como mulher e liderança, construí um negócio sólido apenas com recurso próprio. Crescemos a um CAGR de ~75% ao ano, superamos R$ 678 mil em receita acumulada e já levamos nossas soluções a 14 municípios de 11 estados, tocando a realidade de mais de 41 mil estudantes em projetos educacionais. Fomos validados por grandes parceiros e reconhecidos globalmente no AI4GOOD da Brazil Conference em Harvard/MIT.
>
> Não criei apenas uma empresa de tecnologia; criei um motor de oportunidades para o setor de impacto. Mereço o prêmio porque provo, na prática, que a inovação de ponta só faz sentido quando garante que o impacto no país seja visto, valorizado e multiplicado.

### 13.9 Modelo de negócio híbrido (Sebrae Startups Q3)

**Estrutura:** 2 plataformas proprietárias + transição planejada % serviços → % produto.

**Exemplo:**

> A Manacá opera em modelos B2B e B2G, atuando na transição de um modelo de serviços para um modelo SaaS escalável.
>
> Atualmente, nossa receita é tracionada por consultorias estratégicas em ESG e impacto socioambiental, que validam a dor do mercado e alimentam o desenvolvimento de nossas tecnologias.
>
> Nossa estratégia de escala e recorrência baseia-se em duas plataformas proprietárias:
> - **Flora**: Plataforma de gestão de impacto com planos de assinatura mensal escalonados (Impulso, Estruturação e Estratégico), variando conforme a complexidade e suporte exigidos pelo cliente.
> - **Saíra**: Sistema inteligente de gestão de resíduos com modelo de receita recorrente baseado em assinatura mensal por ponto de monitoramento ativo.
>
> Esse modelo híbrido garante fluxo de caixa imediato (serviços) enquanto constrói a infraestrutura para receita recorrente de alta margem e baixo custo marginal (SaaS).

### 13.10 TAM/SAM/SOM (WOW Batch #34)

**Estrutura:** 3 camadas de mercado quantificadas + tendências macro.

**Exemplo:**

> O mercado de gestão de impacto socioambiental é massivo e crescente:
> - **TAM:** 880 mil organizações do terceiro setor + empresas ESG no Brasil.
> - **SAM:** 21 mil organizações com maturidade digital intermediária.
> - **SOM:** 2 mil organizações acessíveis nos próximos 3 anos.
>
> O mercado global de investimento de impacto atingiu **US$ 1,571 trilhão** (crescimento de 21% a.a.). No Brasil, o investimento social privado (GIFE 2022) movimentou **R$ 4,8 bilhões**.
>
> Para o Saíra (smart cities / resíduos sólidos): **5.570 municípios brasileiros** investem bilhões em gestão de resíduos (PNRS). Recife sozinha possui **1.700+ pontos de descarte irregular**.
>
> A Manacá atua na interseção de três megatendências: transformação digital, exigência crescente de ESG por investidores e reguladores, e políticas públicas baseadas em evidências.

---

## 14. Estilo Manacá — padrões observados em redação bem-sucedida

Padrões recorrentes em inscrições da CEO Rayssa que devem ser replicados quando a skill redigir em nome da Manacá.

### 14.1 Quantificação obsessiva

Cada parágrafo deve ter ao menos **um número concreto**: R$, %, quantidade ou ano. Texto sem números soa como marketing, não como tração.

✅ "Crescemos a um CAGR de ~75% ao ano, superamos R$ 678 mil em receita acumulada e já levamos nossas soluções a 14 municípios de 11 estados."
❌ "Crescemos muito nos últimos anos e estamos em vários estados do Brasil."

> **Métrica de crescimento canônica:** **CAGR ~75% a.a.** (submetido InovAtiva mai/2026). Não usar mais o "140% ao ano" de rascunhos antigos (janela/base diferente, descontinuado).

### 14.2 Hierarquia de listas em "Resultados"

A ordem canônica para campos de "resultados" / "tração" é:
1. ALCANCE E ESCALA (municípios, estados, clientes)
2. IMPACTO QUANTIFICADO (pessoas tocadas, projetos, métricas-fim)
3. CRESCIMENTO FINANCEIRO (faturamento ano-a-ano + acumulado + crescimento %)
4. CAPTAÇÃO VIA EDITAIS (total captado + breakdown por programa/agência/ano)
5. RECONHECIMENTOS (selos, premiações, seleções)
6. ACELERAÇÕES (programas dos quais participou)

### 14.3 Redes sociais e links sempre incluídos

Quando o campo aceita texto livre e há espaço, incluir LinkedIn, Instagram, site, vídeo (YouTube). Cada chancela ganha link verificável.

### 14.4 Citações de chancela explícitas

Sempre citar a instituição completa que chancela:

✅ "AI4GOOD da Brazil Conference at Harvard/MIT (2025)"
✅ "Selo 'Projeto com Propósito' do PMI-ES (2026)"
✅ "Portal Impacta Brasil do MDIC, celeiro de soluções da COP30 (2025)"

❌ "premiado em Harvard"
❌ "selo do PMI"

### 14.5 Verbos no presente para tração, futuro factual para promessa

✅ "Operamos em modelos B2B e B2G."
✅ "O investimento permitirá acelerar o desenvolvimento."

❌ "Estamos podendo operar em B2B e B2G."
❌ "O investimento poderia talvez acelerar..."

### 14.6 Mensagem de fechamento em 3 parágrafos

Para campos do tipo "por que devemos te selecionar", terminar sempre com **3 parágrafos curtos** na sequência **missão → tração → diferencial**, não 1 parágrafo longo.

### 14.7 Cliente sempre com 1 linha de contexto

Listar clientes sem explicar quem são é fraco. Cada cliente citado deve ganhar 1 frase curta de contexto.

✅ "Bbutton: aceleradora de negócios, cliente recorrente."
❌ "Bbutton."

---

## 15. Anti-padrões observados

Padrões que apareceram em rascunhos gerados pela skill e foram corrigidos pela CEO antes da submissão. Evitar.

### 15.1 ❌ "A gente vai..." / "Nós queremos..." em proposta formal

Sempre construções impessoais ou terceira pessoa.

✅ "A empresa executará..."
❌ "A gente vai fazer..."

### 15.2 ❌ Adjetivos hiperbólicos sem prova

Banidos: "revolucionário", "único do mercado", "inédito", "perfeito", "disruptivo" — a menos que demonstrado com especificação técnica explícita.

### 15.3 ❌ Mistura de tom

Não combinar parágrafo formal seguido de parágrafo coloquial. Manter registro consistente do início ao fim.

### 15.4 ❌ Lista de clientes sem contexto

Não citar "Bbutton, Bracell, Suzano" como nomes soltos. Cada um precisa de 1 frase explicativa.

### 15.5 ❌ Inconsistência interna entre documentos

Caso real (abr/2026): a CEO escreveu "Sebrae/MDIC/ABDI" no doc PES e "Sebrae/MDIC/ITA" no doc WOW. Quando a skill detectar variantes do mesmo dado em documentos diferentes do mesmo ciclo, **pausar e perguntar ao usuário** qual é a forma vigente.

### 15.6 ❌ Dados sem ano/data

"Crescemos muito" sem janela temporal é marketing. Sempre citar ano de referência ou faixa.

### 15.7 ❌ ODS genérico

"Alinhado ao ODS 10" é fraco. Citar sub-meta específica: "ODS 10.3 — garantir igualdade de oportunidades..."

### 15.8 ❌ TRL declarado sem evidência

"TRL 7" sem tabela de evidências (número de clientes pagantes, métricas de uptime, datas de validação) é redutível pelo avaliador. Sempre acompanhar TRL com 2-3 evidências documentais.

### 15.9 ❌ Quantidade exata de clientes e faturamento explícito (REGRA — confirmada mai/2026)

**Não declarar a quantidade exata de clientes nem o faturamento/receita explícitos da Manacá/Flora** em propostas/formulários de edital. Usar sempre fraseado **qualitativo**:

- ✅ "base recorrente de clientes pagantes", "carteira diversificada de clientes", "crescimento sustentado de receita ao longo de 3,5 anos"
- ❌ "14 clientes pagantes", "receita acumulada de R$ 678 mil", "CAGR de ~75% a.a.", "faturamento de R$ X"

**Por quê:** dados sensíveis/competitivos, que envelhecem rápido e expõem a empresa a escrutínio desnecessário em texto de proposta. Exceção: quando o **campo do formulário pede explicitamente** o número (ex.: campo "faturamento dos últimos 12 meses", "nº de clientes") — aí preencher com o valor canônico de `empresa-manaca.md`. A regra vale para o **corpo narrativo**, não para campos estruturados que exigem o número.
> Pode citar livremente: **projetos entregues** (track record de entrega), nomes de clientes-âncora com contexto (Suzano, Bracell, etc.), prêmios e o histórico do SAÍRA-CPSI.

---

## 16. Padrões vencedores — InovAtiva de Impacto 2026 (SAÍRA/Flora)

> Fonte: formulário InovAtiva submetido em mai/2026 (texto **azul** = oficial; ver extrato em
> `c:\Editais\editais\inovativa-impacto-2026\_inovativa-AZUL.md`). Estes são padrões de redação
> de alto nível, já vetados pela CEO, reaproveitáveis em qualquer edital de impacto/inovação.

### 16.1 "Impacto é engrenagem, não subproduto" (tese de mudança)
Amarrar receita à geração de impacto de forma que **tirar o impacto inviabilize o negócio**.
> "A receita gerada por ponto monitorado está diretamente indexada ao sucesso da triagem e do redirecionamento logístico do resíduo. […] Tirar o impacto socioambiental da nossa operação inviabiliza o negócio, pois o que o mercado compra é a infraestrutura para transformar dados dispersos em decisões verificáveis."

### 16.2 Estrutura de 5 partes para "superioridade ao status quo"
1. **Status quo** (como o problema é resolvido hoje, com tempos/custos: "ciclo de 24–72h, sem georreferenciamento") → 2. **Inovação técnica** (o que muda, quantificado: "5–30 min, redução de 1–2 ordens de magnitude") → 3. **Disrupção no modelo de negócio** (CPSI, assinatura por ponto) → 4. **Aplicabilidade adjacente** (B2B sem ramificar roadmap) → 5. **Posição competitiva** (concorrentes nomeados + por que não cobrem o problema).

### 16.3 CPSI como instrumento replicável
Enquadrar o CPSI (LC 182/2021) não como "um contrato", mas como **modelo jurídico replicável**: "cada novo município é um CPSI replicável, não uma venda tradicional". Sempre citar o caso Recife (dez/2025, R$50k MVP → até R$1,6 mi aceleração → até R$8 mi fornecimento) como prova de execução.

### 16.4 "Propriedade da inteligência"
Ao usar tecnologia aberta de base (YOLO, LLMs, cloud), deixar explícito que **a inteligência é proprietária**: "Usamos YOLO como arquitetura aberta de base — mas o modelo treinado, os pesos finais, o pipeline de inferência e a lógica de classificação são proprietários." Ancorar no **dataset proprietário** (10.000+ imagens, 12 categorias) e na **XAI com lineage de dado e citação de fonte**.

### 16.5 Validação em três camadas
Para "validação de mercado", combinar: (a) **piloto formal em ambiente real** (CPSI Recife, entregas técnicas listadas); (b) **receita recorrente diversificada** (3,5 anos, 14 clientes, CAGR ~75%, nomes-âncora: Suzano, Bracell, Fundo Vale, Instituto Arco, Ensina Brasil, Bbutton); (c) **reconhecimento externo** (AI4GOOD Harvard/MIT, CADIMPACTO Ouro, selos).

### 16.6 "Escalar sem diluir o impacto"
Três mecanismos: (1) **replicabilidade jurídico-financeira** (CPSI + verticais B2B regulatórios); (2) **padronização metodológica via Flora** (mesma régua de auditoria); (3) **rede de cooperativas locais fortalecida, não substituída** ("a receita B2B premium não dilui o impacto: ela o financia"). Vetor regulatório citado em cada vertical (PNRS, logística reversa, Novo Marco do Saneamento) para mostrar **demanda recorrente compulsória**.

### 16.7 Convenção de cor no Caderno de Preenchimento (lição operacional)
No InovAtiva, a CEO usou **azul = texto final submetido**, deixando versões alternativas (prosa longa, condensada) em outras cores. **Lição:** ao montar Caderno com múltiplas versões de uma resposta, marcar a versão final em cor única acordada — e, ao extrair "o que foi submetido", filtrar só essa cor (a API do Google Docs expõe `foregroundColor`; o export markdown perde a cor).