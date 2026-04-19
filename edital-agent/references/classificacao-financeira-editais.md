# Classificação Financeira em Formulários de Editais

> Decisões financeiras recorrentes em formulários quantitativos (FINEP FAP, FAPs estaduais, subvenção). Complementa [matriz-agencias-equipe.md](matriz-agencias-equipe.md) — aquela cobre regras por agência (quem pode receber pró-labore, etc.); este documento cobre **como classificar cada valor** nos campos do formulário.

## Quando consultar

Ao preencher qualquer formulário com:
- Tabela "Receita Bruta / Lucro Líquido / % Exportação" por ano
- Tabela "Fontes de recursos além da geração própria de caixa"
- Tabela "Custos e despesas fixos"
- Pergunta "% da Receita Bruta decorrente de novos produtos ou significativamente melhorados"
- Tabela "Investimento para a inovação"

## 1. Faturamento vs Captação

O formulário separa **receita operacional** (Faturamento / Receita Bruta) de **entrada de recursos externos** (Captação / Fontes de recursos além da geração própria de caixa).

| Origem do recurso | Classificação | Exemplo |
|---|---|---|
| Cliente pagando por serviço ou produto entregue | **Faturamento** | Consultoria a Bracell, SaaS Flora para Bbutton |
| Contrato com órgão público ganho via processo competitivo (CPSI, pregão, licitação) | **Faturamento** | SAÍRA CPSI com Prefeitura do Recife (R$ 50k) |
| Prêmio/reconhecimento em dinheiro sem contrapartida de serviço | **Captação** → Outras externas | Shell Iniciativa Jovem |
| Edital de subvenção econômica | **Captação** → FINEP ou Instituições de fomento | Seedes (Neo Ventures, ES), CPSI Mais Inovação Brasil |
| Edital de fomento sem obrigação de serviço | **Captação** → Instituições de fomento | Centelha ES, Programa Nacional Empreendedoras Tech |
| Empréstimo/financiamento bancário | **Captação** → Bancos públicos | BNDES, BRDE |
| Aporte de investidor (anjo, fundo, equity) | **Captação** → Investidores privados | Fundos VC, anjos |
| Sócio colocando dinheiro na empresa | **Captação** → Recursos dos sócios | Capital próprio investido, custos pagos com conta pessoal |

### Regra de bolso: "Edital vs Contrato"

> **Se há contrapartida contratual de serviço entregue a quem pagou** → é faturamento.
>
> **Se é prêmio/fomento sem contrapartida de serviço** → é captação.

Confusão comum (vista na sessão Mulheres Inovadoras 2026-04-19): "SAÍRA CPSI R$ 50k" pode parecer edital pelo nome, mas é **contrato de prestação de serviço** com a Prefeitura. Vai em Faturamento.

## 2. Reembolso de Sócios ≠ Recursos dos Sócios

**Muito comum confundir**:

| Movimento | Direção | Classificação |
|---|---|---|
| Sócio paga despesa da empresa com dinheiro pessoal | Entra na empresa | **Recursos dos sócios** (em Fontes de recursos) |
| Sócio integraliza capital | Entra na empresa | **Recursos dos sócios** |
| Empresa devolve ao sócio valor que ele adiantou | Sai da empresa | Despesa — **não é** fonte de recurso |

Na sessão: linha "Reembolso sócios R$ 9.000" na planilha era **saída**. A fonte de recurso equivalente (R$ 9.000 "Capital próprio investido" em ago/2025) era a **entrada real**.

## 3. Pró-labore vs Retirada de Lucro

Árvore de decisão:

```
A empresa teve LUCRO LÍQUIDO POSITIVO no período?
├─ SIM: pode distribuir lucros — mas:
│       - Sócio-administrador ainda deve receber pró-labore mínimo (INSS)
│       - Em edital FINEP: declarar pró-labore + distribuição de lucro é transparente
│       - Em edital FAP estadual: checar matriz-agencias-equipe.md (alguns vedam pró-labore)
│
└─ NÃO (prejuízo ou zero): pró-labore é a única forma juridicamente segura
        - Distribuir "lucro" sem lucro contábil é irregular (Receita Federal vê como omissão de pró-labore + autuação)
        - Declarar como pró-labore no formulário mesmo que hoje esteja classificado como retirada
        - Ajustar a classificação contábil com o contador para o mês seguinte (sem retroagir)
```

### Nuance operacional

Se a sócia-administradora hoje "faz retirada de lucro" informalmente, mas a empresa teve prejuízo:

1. **No formulário do edital**, declarar como **pró-labore** (descrição correta do fato econômico — remuneração da administradora).
2. **Depois da submissão**, ajustar com o contador para os meses seguintes — não é necessário retroagir para efeito do formulário.
3. Isso **não é mentir**: é classificar o movimento corretamente segundo a natureza econômica.

Referência: CPC 30 (Receitas) + Lei 11.638/2007.

## 4. Empresa Remota → Aluguel/Luz/Água/Telefone = R$ 0

Formulários FINEP e de FAPs pedem breakdown de custos fixos em rubricas padrão:

- Salários (CLT)
- Pró-labore
- Aluguel
- Luz
- Água
- Telefone
- Outros

Se a empresa opera 100% remota:

| Rubrica | Valor esperado |
|---|---|
| Aluguel / Luz / Água / Telefone | **R$ 0 em todos os meses** |
| Outros | Concentra contabilidade, softwares/SaaS, serviços de assinatura, viagens para clientes, PJs fixos (desenvolvedores, analistas) |

Declarar zero é legítimo e **esperado** para startups modernas. Na descrição de "Outros", explicitar: *"Manacá opera em regime 100% remoto, sem custos com aluguel, luz, água ou telefonia empresarial."*

## 5. % Receita Bruta com Produtos Novos ou Significativamente Melhorados

Formulários quantitativos pedem essa métrica para avaliar maturidade de produto. Classificação:

| Tipo de receita | Conta como "produto novo/melhorado"? |
|---|---|
| SaaS proprietário com cobrança recorrente | **Sim** — 100% |
| Licenciamento de software próprio | **Sim** — 100% |
| Contrato de serviço usando metodologia proprietária da empresa | **Depende** — se é entrega de produto embarcado, conta; se é hora-homem de consultoria, não |
| Consultoria tradicional (hora técnica, entrega de relatório) | **Não** — serviço, não produto |
| Contrato público de prestação de serviço com entrega de software/hardware | **Sim** se há produto entregue (ex.: SAÍRA CPSI conta porque entrega sistema + hardware) |
| Treinamentos / formações | **Não** — serviço |

### Framing estratégico: curva 0% → 40% → 75%

Uma empresa em transição de consultoria para produto terá naturalmente uma curva baixa no passado e crescente no futuro. **Isso não é fragilidade — é prova de disciplina de pivot.**

Narrativa a adotar em Critérios II/III:

> *"A empresa consolidou caixa via consultoria [ANOS X-Y], reinvestindo resultado em P&D dos produtos [A e B]. [ANO Z] marca o pivot formal para empresa de produto, com [N]% da receita oriunda de SaaS proprietário. Expectativa de [N]% em [ANO Z+1] e [N]% em [ANO Z+2], consolidando o perfil de empresa de produto."*

Exemplo vivo: Manacá em 2026 (sessão Mulheres Inovadoras) declarou 0% em 2023-2025 e 40% em 2026, com projeções 60% (2027) e 75% (2028). Ver `05a-data-pack.md` daquele edital.

## 6. Investimento para a Inovação (histórico por ano)

Formulários pedem descrição + valor por ano em P&D. Rubricas típicas que contam:

- Pessoal dedicado a P&D (desenvolvedor, pesquisador — mesmo PJ)
- Equipamentos e instrumentos para protótipo
- Infraestrutura de nuvem para desenvolvimento
- Licenças de softwares de desenvolvimento e análise
- Ferramentas de design e prototipação
- Viagens para validação com clientes-alvo
- Tempo parcial dos sócios alocado em P&D (pode ser estimado)

**Não incluir**: despesas gerais, marketing, vendas, contabilidade (essas entram em "Custos e despesas fixos" ou "Marketing" no Plano de Investimentos).

## Checklist ao aplicar

- [ ] Revisar cada linha de captação: é edital sem contrapartida (captação) ou contrato com entrega (faturamento)?
- [ ] Conferir se há reembolso de sócio confundido com recurso de sócio
- [ ] Se o sócio-administrador é remunerado como "retirada de lucro" em empresa com prejuízo: reclassificar para pró-labore
- [ ] Aluguel/luz/água/telefone = R$ 0 declarado explicitamente se for empresa remota
- [ ] % de produto novo consistente com o que é declarado em Critério III (inovação)
- [ ] Investimento em inovação inclui tempo de sócios + PJs + infra + licenças

## Referência viva

Ver `05a-data-pack.md` do edital [Mulheres Inovadoras FINEP 2026](c:/Editais/editais/premio-mulheres-inovadoras-finep-2026/05a-data-pack.md) para o exemplo completo com todas essas decisões aplicadas a uma empresa real.
