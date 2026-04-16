# Plano de Formação e Contratação de Equipe

**Uso:** preencher na Fase 05c.2 **quando** o projeto depende de contratações pagas pelo fomento. Tipicamente Trilha B (subvenção com orçamento substantivo). Dispensável em Trilha A (prêmios).

**Princípio:** omitir a equipe futura ou descrevê-la vagamente é uma falha estrutural. O avaliador precisa ver que você já pensou no perfil, no momento e na estratégia de recrutamento.

---

## Bloco 1 — Resumo das Vagas a Contratar

| # | Cargo | Dedicação | Mês de Contratação | Rubrica | Custo Total no Projeto |
|---|---|---|---|---|---|
| 1 | {CARGO} | {X}h/semana | M{Y} | Pessoal e Encargos | R$ {Z} |
| 2 | {CARGO} | {...} | {...} | {...} | {...} |

**Exemplo:**

| # | Cargo | Dedicação | Mês | Rubrica | Custo |
|---|---|---|---|---|---|
| 1 | Cientista de Dados Pleno | 40h/semana | M3 | Pessoal e Encargos | R$ 180.000 (18 meses) |
| 2 | Engenheiro de Dados Júnior | 30h/semana | M4 | Pessoal e Encargos | R$ 96.000 (16 meses) |
| 3 | Bolsista TT-3 (via FAPESP) | 20h/semana | M2 | Bolsa (se FAPESP) | R$ 30.000 (20 meses) |

---

## Bloco 2 — Ficha Detalhada Por Vaga

Replicar este bloco para cada contratação planejada:

### Vaga {#X}: {CARGO}

**Dedicação:** {X}h/semana
**Regime:** CLT / Bolsista / PJ de P&D
**Mês de contratação no cronograma:** M{Y}
**Rubrica orçamentária:** Pessoal e Encargos (ou Bolsas, conforme agência)
**Atrela-se a qual(is) Meta(s):** M{A}, M{B}

#### Perfil Profissiográfico

**Formação mínima requerida:**
- {ÁREA DE GRADUAÇÃO}
- (Desejável: {PÓS-GRADUAÇÃO, se aplicável})

**Anos de experiência mínima:** {X}

**Competências técnicas exigidas:**
- {COMPETÊNCIA 1}
- {COMPETÊNCIA 2}
- [...]

**Competências desejáveis:**
- [...]

#### Impacto Esperado na Meta

{Parágrafo de 3-5 linhas explicando como essa contratação destrava a Meta X:
"A Meta X depende de [especialidade]. A contratação deste profissional no M{Y}
permite [resultado específico], sem o qual o cronograma atrasaria em N meses."}

#### Estratégia de Recrutamento

- Canais: {LinkedIn, rede de alumni, parques tecnológicos específicos, comunidades técnicas}
- Parcerias para prospecção: {TecVitória, PMI-ES, Impact Hub, universidades parceiras}
- Processo: {triagem → entrevista técnica → teste prático → fit cultural}
- Tempo estimado do processo: {X} semanas
- Plano de contingência em caso de atraso: {ICT parceira temporária / PJ de P&D transitório / ampliação de dedicação interna}

#### Governança Após Contratação

- Reporte direto para: {CTO | Pesquisador Responsável | etc.}
- Onboarding: {X semanas, com plano definido}
- Milestones de avaliação: {M+1 = entrega X; M+3 = entrega Y}

---

## Bloco 3 — Cronograma Consolidado de Contratações

```
Mês:    1   2   3   4   5   6   7   8   9   10  11  12  ...
Vaga 1:             [===Contratação===|==============Execução==============>]
Vaga 2: [Recrutamento|=====================Execução=======================>]
Vaga 3:         [TT Bolsa|==========================Execução==============>]
```

**Exemplo preenchido:**

```
Mês:         1   2   3   4   5   6   7   8   9   10  11  12  ...
Cientista Dados Pleno:       [=contratação=|======================execução======================>]
Eng Dados Júnior:    [recrut.|===============================execução===============================>]
Bolsista TT-3:             [bolsa|===================================execução==============================>]
```

---

## Bloco 4 — Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Atraso na contratação do Cientista de Dados Pleno | Média | Alto (trava M3) | Iniciar processo 60 dias antes; backup via ICT parceira |
| Perfil júnior não atinge produtividade esperada | Média | Médio | Mentoria do CTO; plano de onboarding de 8 semanas |
| Custo de mercado acima do orçado | Baixa | Médio | Orçamento com faixa de ±15% já negociado; bolsa TT como alternativa |

---

## Bloco 5 — Declaração de Internalização (blindagem do core)

Texto-modelo para incluir na narrativa:

> "As contratações planejadas destinam-se exclusivamente a **internalizar capacidade técnica** na Manacá. Os profissionais serão contratados em regime CLT [ou: alocados na rubrica Pessoal e Encargos conforme normativa FINEP], vinculando-se à sede da empresa em {CIDADE}/{UF}. Essa decisão preserva o core tecnológico internamente e garante retenção de conhecimento após o término do projeto, evitando o anti-padrão de terceirização do núcleo criativo vedado pela {AGÊNCIA}."

**Quando esse parágrafo é especialmente relevante:**
- Editais FINEP (regra explícita sobre capacidade absortiva).
- Editais com >25% do orçamento em terceiros (para deixar claro que o core é interno).
- Propostas com ICT parceira (reforça que a ICT está na periferia, não no core).

---

## Checklist Final

- [ ] Cada vaga tem ficha completa (perfil + mês + rubrica + estratégia)
- [ ] Somatório de custos bate com a rubrica "Pessoal e Encargos" do orçamento
- [ ] Mês de contratação é realista (não M1 do projeto — processos levam 6-10 semanas)
- [ ] Estratégia de recrutamento cita canais concretos (não genéricos)
- [ ] Plano de contingência para atraso está descrito
- [ ] Declaração de internalização do core está explícita
- [ ] Regime (CLT / Bolsa / PJ) respeita regras da agência (ver `matriz-agencias-equipe.md`)
