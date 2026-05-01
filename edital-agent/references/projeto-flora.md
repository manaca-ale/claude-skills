---
last_verified: 2026-05-01
next_review: 2026-08-01
type: data
canonical_for:
  - flora_descricao
  - flora_trl
  - flora_clientes
  - flora_stack_tecnologica
  - flora_ativos_reusaveis
derived_from: []
stale_fields:
  - trl ([PERGUNTAR-AO-USUÁRIO] estimativa TRL 6-7 com base em projetos validados, mas precisa confirmação técnica)
  - stack_tecnologica ([PERGUNTAR-AO-USUÁRIO] linguagens, frameworks, infra cloud, modelos IA usados)
  - usuarios_ativos ([PERGUNTAR-AO-USUÁRIO] número exato de usuários ativos hoje)
  - registro_software_inpi ([PERGUNTAR-AO-USUÁRIO] status atual do depósito)
  - patente ([PERGUNTAR-AO-USUÁRIO] confirmar se há patente prevista ou apenas registro de software)
  - pricing_planos_valores ([PERGUNTAR-AO-USUÁRIO] valor R$/mês de cada plano: Impulso, Estruturação, Estratégico)
---

# Projeto Flora — Plataforma de Monitoramento e Gestão de Impacto

## Resumo

Flora é uma plataforma SaaS (Software as a Service) desenvolvida pela Manacá Tecnologias Sociais para monitoramento e gestão de impacto socioambiental, educacional e de sustentabilidade. Integra dados de múltiplas fontes, organiza métricas e indicadores validados e utiliza inteligência artificial para gerar análises preditivas, relatórios e dashboards interativos.

## Status Atual

| Campo | Valor |
|-------|-------|
| TRL (Technology Readiness Level) | [PERGUNTAR-AO-USUÁRIO: TRL atual com evidências] — estimativa baseline TRL 6-7 (MVP em validação com primeiros clientes SaaS) |
| Stack Tecnológica | [PERGUNTAR-AO-USUÁRIO: linguagens, frameworks, infra cloud, modelos IA] |
| Usuários ativos | [PERGUNTAR-AO-USUÁRIO: número exato] — Bbutton confirmado como cliente recorrente com 2 projetos |
| Servidor | EC2 AWS (alias SSH: Flora) |
| Reconhecimento | **Selo "Projeto com Propósito" — PMI-ES (2026)** |
| Status comercial | Primeiros clientes SaaS em validação (Bbutton recorrente) — transição bootstrapped consultoria → produto |

## Funcionalidades

### Módulos Principais
1. **Teoria da Mudança / Modelo Lógico** — Representação visual da lógica de intervenção
2. **Menu de Métricas e Indicadores** — Biblioteca de indicadores validados cientificamente
3. **Coleta de Dados** — Instrumentos de coleta integrados (surveys, formulários)
4. **Análise de Dados e Dashboards** — Painéis interativos para visualização e monitoramento
5. **Plano de Indicadores** — Planejamento e sistemática de monitoramento
6. **Biblioteca de Evidências** — Acesso a modelos e indicadores validados
7. **Relatórios automatizados com IA** — Geração inteligente de relatórios de impacto

### Três Eixos de Atuação
1. **Estratégia** — Construção de estratégias de impacto (métricas claras, teoria de mudança)
2. **Gestão de Dados** — Co-criação de instrumentos de coleta, validação de fluxos
3. **Impacto** — Tradução de dados em insights acionáveis (dashboards, relatórios técnicos)

### Camada de Inteligência Artificial

A Flora aplica IA em três modalidades complementares:

| Modalidade | Aplicação | Estado |
|------------|-----------|--------|
| IA Generativa (LLMs) | Geração automática de relatórios de impacto em linguagem simples; síntese de dados qualitativos | Em produção |
| IA Preditiva | Cruzamento de indicadores para projeções de impacto futuro | Em validação |
| IA Explicável (XAI) | Auditabilidade dos resultados gerados pela IA — diferencial vs. ChatGPT genérico | Em validação |
| Integração APIs públicas | IBGE, AdaptaBrasil, GIFE — enriquecimento automático de datasets | Em produção |

## Diferencial Competitivo

| Manacá / Flora | Consultorias Tradicionais | Plataformas ESG |
|----------------|--------------------------|-----------------|
| Sistema integrado com governança de dados e segurança da informação | Não possuem sistema integrado | Não possuem inteligência e evidências para comprovação de impacto real |
| Abordagem 360° (estratégia + dados + impacto) | Foco fragmentado | Foco em compliance, não em impacto real |

## ICP — Ideal Customer Profile (v0)

**Tipo de organização ideal:** Organizações intermediárias e gestoras de portfólios de impacto socioambiental que precisam centralizar, mensurar e comunicar resultados.

### 5 Segmentos Atendidos

1. **Fundações e Institutos Empresariais** — Ex: Fundação Arymax, Instituto Sabin, Fundação Tide Setubal
2. **Aceleradoras, Incubadoras e Redes de Impacto** — Ex: Quintessa, Artemisia, ICE, Sistema B
3. **ONGs estruturadas e OSCs com múltiplos projetos** — Redes locais apoiadas por fundações
4. **Organizações Públicas, Bancos de Fomento e Agências** — Ex: Sebrae, BNDES, secretarias estaduais
5. **Empresas com Programas de ISP** — Corporações com institutos próprios ou programas ESG

### Características do cliente ideal

| Elemento | Descrição |
|----------|-----------|
| Setor principal | Impacto socioambiental, sustentabilidade, inovação social |
| Tamanho médio | 10-200 colaboradores, múltiplos projetos simultâneos |
| Maturidade digital | Intermediária (planilhas, ferramentas desconectadas) |
| Necessidades centrais | Padronizar dados, automatizar relatórios, comunicar impacto |
| Motivadores de compra | Pressão por resultados, eficiência, diferenciação competitiva |

## Personas v0

### Persona 1: Ana Paula — Gestora de Impacto
- 38 anos, gerente/coordenadora em fundação ou incubadora
- Formação em ciências sociais ou administração
- **Dores:** dados vindos de diferentes parceiros, falta de equipe técnica, consultorias externas caras
- **Motivações:** autonomia, mostrar resultados ao conselho/investidores, ferramentas práticas
- **Comportamento:** LinkedIn, newsletters GIFE/ICE, eventos de inovação social

### Persona 2: Gestora de Sustentabilidade (setor privado)
- **Dor:** indicadores dispersos, falta de tempo para comprovar impacto ESG
- **Busca:** resultados auditáveis, dashboards alinhados a GRI/ISSB/ODS

### Persona 3: Coordenadora de Projetos (ONGs)
- **Dor:** falta de equipe técnica, dificuldade de captar recursos com evidências
- **Busca:** profissionalizar gestão de impacto, modelos prontos de TdM

### Persona 4: Gestor Público
- **Dor:** dados fragmentados entre secretarias
- **Busca:** melhorar políticas públicas com base em evidências

## Pricing

Modelo atual (atualizado conforme inscrição Sebrae Startups 2026): **três planos de assinatura mensal escalonados** + consultoria estratégica.

| Plano | Foco | Público-alvo | Valor R$/mês |
|-------|------|--------------|--------------|
| **Impulso** | Onboarding e gestão básica de impacto | ONGs e Institutos com 1-2 projetos | [PERGUNTAR-AO-USUÁRIO] |
| **Estruturação** | Múltiplos projetos + dashboards + suporte | Fundações e aceleradoras com portfólio | [PERGUNTAR-AO-USUÁRIO] |
| **Estratégico** | Customização total + IA preditiva + suporte dedicado | Grandes institutos, empresas com ISP, governos | [PERGUNTAR-AO-USUÁRIO] |
| Consultoria estratégica | Projetos discretos (Teoria da Mudança, SROI, dashboards) | A partir de R$ 3.000,00 (ticket médio R$ 16.000,00) |
| Modelo de aquisição | Freemium para diagnóstico → conversão para plano pago |

> **Nota crítica:** os valores R$/mês de cada plano variam conforme negociação com o cliente. Antes de declarar valor em formulário de edital, **perguntar à Rayssa** o valor vigente do plano em questão. Histórico legado (não usar): plano Básico R$ 49,90 / Completo R$ 299,00 — descontinuado.

## Concorrentes

### Concorrentes Diretos

| Concorrente | Preço | Diferencial | Limitação |
|-------------|-------|-------------|-----------|
| Move Social | R$ 300/mês | Plataforma de gestão de projetos sociais | Funcionalidades simples, sem IA, sem governança de dados |
| Sopact | US$ 99/mês | Consultoria + plataforma cloud | Fora do Brasil, foco em compliance ESG (não impacto real) |
| Bússola Social | Sob consulta | Inteligência e personalização | Modelo consultoria, sem plataforma SaaS escalável |

### Concorrentes Indiretos

| Concorrente | Posicionamento | Limitação vs. Manacá |
|-------------|----------------|----------------------|
| **IDIS** | Consultoria tradicional de impacto | Caros, não escaláveis, sem tecnologia proprietária |
| **McKinsey Social** | Big consultancy | Caros, sem plataforma, projetos longos |
| ChatGPT / IA genérica | Geração de texto livre (~R$ 120/mês) | Sem metodologia validada para mensuração de impacto, sem segurança de dados, sem auditabilidade |

### Diferenciais Manacá/Flora

1. **IA Explicável (XAI):** A Flora não apenas armazena dados — interpreta e gera relatórios confiáveis e auditáveis automaticamente.
2. **Aderência local + LGPD:** Integração nativa com bases públicas brasileiras (IBGE, AdaptaBrasil) e total segurança/privacidade de dados.
3. **Custo-benefício:** Operação até 80% mais acessível que modelos tradicionais de consultoria.
4. **Abordagem 360°:** Estratégia + dados + impacto em uma plataforma só, vs. soluções fragmentadas.
5. **Validação enterprise:** Clientes como Suzano, Bracell e Prefeitura do Recife (CPSI).

## Posicionamento de Marca

- **Frase-síntese:** "Flora organiza a complexidade do impacto para apoiar decisões que importam."
- **Definição:** Sistema de gestão de impacto orientado por dados
- **Essência:** Dados com sensibilidade, impacto com método
- **Identidade visual:** Formas orgânicas abstratas sobrepostas representando sistema vivo de dados; gradientes simbolizam integração; espaço entre formas comunica clareza e transparência

## Projetos Validados

### 1. Cachoeiro de Itapemirim (ES) — Monitoramento Educacional
- **Parceiro:** ES em Ação
- **Escopo:** Monitoramento de escolas de tempo integral
- **Entregas:** Metodologia, 13 indicadores de impacto educacional, dashboard, relatório final
- **Status:** Concluído com aprovação

### 2. Bracell Bahia — Avaliação de Impacto Social
- **Projetos:** Farmácia Verde e Educação Continuada
- **Entregas:** Teoria de Mudança, sistemática de monitoramento, pesquisa de campo, relatórios
- **Status:** Concluído

### 3. Instituto Aprender Cultura (IAC)
- **Escopo:** Teoria da Mudança + Métricas e Indicadores
- **Entregas:** Análise contextual, oficinas de validação, métricas de impacto
- **Status:** Concluído

### 4. Sintetizo / Bridge Gestão Social
- **Escopo:** Validação de metodologias, oficina de Teoria de Mudança
- **Entregas:** Revisão de 3 Teorias de Mudança, 3 pacotes de métricas
- **Status:** Concluído

### 5. Ensina Brasil
- **Escopo:** Logística de pesquisas + elaboração de indicadores
- **Entregas:** 2 contratos de parceria
- **Status:** Concluído

## Roadmap 2026

| Trimestre | Foco |
|-----------|------|
| 1º tri | MVP Robusto & Primeiros Contratos: versão Beta, relatórios automatizados com IA |
| 2º tri | Escala Inicial: módulo de gestão de resíduos (Saíra), desenho metodológico (storytelling de impacto) |
| 3º tri | Automação & Recorrência: benchmark setorial, motor de recomendação, alertas automáticos |
| 4º tri | Consolidação & Expansão: 25+ clientes ativos, aprimoramento da IA |

## Mercado Endereçável (TAM/SAM/SOM)

Quantificação canônica (atualizada com inscrição WOW Batch #34, abr/2026):

| Camada | Tamanho | Composição |
|--------|---------|-------------|
| **TAM (Total Addressable Market)** | 880 mil organizações | Terceiro setor + empresas com programa ESG no Brasil |
| **SAM (Serviceable Addressable Market)** | 21 mil organizações | Subset com maturidade digital intermediária (planilhas + ferramentas desconectadas) |
| **SOM (Serviceable Obtainable Market — 3 anos)** | 2 mil organizações | Subset acessível via canais atuais da Manacá |
| Mercado global de investimento de impacto | US$ 1,571 trilhão | GIIN 2025 — crescimento 21% a.a. |
| Investimento social privado Brasil (GIFE) | R$ 4,8 bilhões | Edição 2022 do Censo GIFE |

## Proposta de Valor para Editais

A Flora se posiciona na interseção de:
- **Transformação Digital** — Plataforma SaaS com IA para gestão de dados
- **Impacto Socioambiental** — Mensuração e evidência de impacto real
- **Governança ESG** — Compliance e transparência para investidores e governo
- **Políticas Públicas baseadas em evidências** — Apoio à decisão com dados

### ODS Relacionados
- ODS 4: Educação de Qualidade
- ODS 11: Cidades e Comunidades Sustentáveis
- ODS 13: Ação contra a Mudança Global do Clima
- ODS 16: Paz, Justiça e Instituições Eficazes
- ODS 17: Parcerias e Meios de Implementação

## Propriedade Intelectual

| Campo | Valor |
|-------|-------|
| Registro de software | [PERGUNTAR-AO-USUÁRIO: status do depósito INPI] — em processo |
| Patentes | [PERGUNTAR-AO-USUÁRIO: confirmar se há intenção de patente] |
| Marca registrada "Flora" | Em processo de depósito no INPI |
| Código-fonte | Proprietário da Manacá (proteção Lei 9.610/98 + acordos confidencialidade com PJs) |

## Ativos Reutilizáveis

Materiais já produzidos do Flora que podem ser reaproveitados em editais futuros (vídeos, imagens, decks, PDFs branded). Quando um edital pede pitch/visual/dossiê, conferir aqui antes de criar do zero.

| Tipo | Descrição | Caminho/Link |
|------|-----------|--------------|
| _(placeholder)_ | _Adicionar conforme produzir ativos para Flora_ | _[PERGUNTAR-AO-USUÁRIO: lista de ativos disponíveis (vídeos, decks, screenshots Flora) com caminho/link]_ |

**Convenção:** ao reaproveitar um ativo, copiar para o diretório do novo edital (não link cross-projeto). Atualizar esta tabela quando produzir asset novo significativo (cover, vídeo, deck, imagem hero).
