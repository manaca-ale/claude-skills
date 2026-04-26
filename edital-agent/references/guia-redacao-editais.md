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