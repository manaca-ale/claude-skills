# ICTs Parceiras — Template de Documentação

**Uso:** preencher na Fase 05c.2 **quando** o projeto envolver parceria com Instituições de Ciência e Tecnologia (universidades, institutos de pesquisa, laboratórios certificados). Exigido em arranjos em rede FINEP, Nova Economia Capixaba (FAPES), Redes de Inovação FACEPE, etc.

**Decisão da Manacá (2026-04):** este template cobre apenas **ICTs**. Não tratamos advisors formais com equity/vesting nesta versão.

**Princípio da periferia do risco:** a tecnologia central (core) permanece interna. A ICT atua na periferia — certificações, laudos, ensaios, acesso a equipamentos. **Violar esse princípio é anti-padrão fatal** ("Terceirização da Inteligência Central").

---

## Bloco 1 — Cadastro da ICT

### ICT #{X}: {NOME INSTITUIÇÃO}

**Razão social / CNPJ:** {...}
**Natureza:** {Universidade Federal | Universidade Estadual | Universidade Privada | Instituto Federal | Centro de Pesquisa | Unidade EMBRAPII | Outro}
**Localização:** {Cidade / UF}
**Credenciamento relevante:** {ex: Unidade EMBRAPII, laboratório ISO/IEC 17025, INMETRO, etc.}

**Representante institucional para o projeto:**
- Nome: {...}
- Cargo: {Pró-Reitor de Pesquisa | Coordenador de Departamento | Diretor de Centro}
- Contato: {email}

**Pesquisador principal vinculado (da ICT):**
- Nome: {...}
- Titulação: {Doutor em X, Mestre em Y}
- Lattes: {URL}
- Cargo na ICT: {Professor Associado, Pesquisador Sênior, etc.}
- Grupo de pesquisa / Laboratório: {...}

---

## Bloco 2 — Atividades Específicas (Periferia do Risco)

**Regra:** as atividades da ICT devem ser **auxiliares e não-nucleares**. Exemplos aceitáveis:

- Certificação em ambiente simulado (TRL 5+)
- Ensaios destrutivos sob normas ISO/ABNT
- Validações clínicas / laboratoriais
- Acesso a equipamentos multiusuários raros (microscópio eletrônico, câmara anecoica, etc.)
- Laudos técnicos isentos
- Benchmarks matemáticos / estatísticos
- Treinamento de equipe da empresa
- Uso de infraestrutura de supercomputação

**Exemplos que caracterizam anti-padrão (evitar):**

- ICT "desenvolvendo o algoritmo" (core = interno)
- ICT "escrevendo o software" (core = interno)
- ICT "desenhando a arquitetura" (core = interno)

### Lista de atividades da ICT #{X}:

| Atividade | Meta do projeto | Entregável | Mês | Evidência de isenção/imparcialidade |
|---|---|---|---|---|
| {...} | M{Y} | {laudo / relatório / certificado} | M{Z} | {norma aplicada, equipamento calibrado, etc.} |

**Exemplo:**

| Atividade | Meta | Entregável | Mês | Evidência |
|---|---|---|---|---|
| Ensaio de durabilidade do sensor IoT sob ciclagem térmica | M4 | Laudo técnico conforme ABNT NBR IEC 60068-2-14 | M5 | Laboratório acreditado RBLE + equipamento com calibração válida |
| Validação estatística do modelo de classificação | M3 | Relatório de performance com IC 95% | M4 | Análise cega por estatístico PhD independente da equipe de desenvolvimento |

---

## Bloco 3 — Rubrica Orçamentária

**NUNCA** alocar a ICT na aba "Equipe Executora" da FINEP ou no cadastro de bolsistas da FAPESP. ICTs vão em **rubricas separadas**:

| Agência | Rubrica correta | Limites |
|---|---|---|
| FINEP | Serviços de Terceiros — Pessoa Jurídica | Arranjos em rede: mín 5% para ICT |
| FAPESP PIPE Fase 1 | Serviços de Terceiros | Máx 1/3 do orçamento |
| FAPESP PIPE Fase 2 | Serviços de Terceiros | Máx 1/2 do orçamento |
| EMBRAPII | Contrapartida da Unidade EMBRAPII | Segue edital específico |
| FAPs estaduais | Varia | Consultar edital |

### Orçamento alocado para ICT #{X}:

- Valor total: R$ {...}
- Distribuição: {detalhar por atividade/entregável}
- % do orçamento total do projeto: {...}%

---

## Bloco 4 — Documentação Mandatória (anexos)

Sem esses documentos, a proposta é desclassificada em triagem preliminar:

### Documentos da ICT:

- [ ] **ACT** (Acordo de Cooperação Técnica) assinado pelo representante institucional — OU minuta pré-acordada com previsão de assinatura após aprovação.
- [ ] **Carta de Anuência Institucional** assinada pelo Pró-Reitor (ou autoridade equivalente).
- [ ] **Carta de Anuência Individual** assinada pelo pesquisador principal da ICT.
- [ ] **Lattes do pesquisador principal** atualizado (≤6 meses).
- [ ] **Comprovante de credenciamento** (quando aplicável — ex: certificação Unidade EMBRAPII, ISO, etc.).

### Documentos da Manacá:

- [ ] Termo de ciência da contratação de serviços de terceiros (quando exigido).
- [ ] Declaração de não-alienação de PI.

---

## Bloco 5 — Declaração de Blindagem do Core (parágrafo-modelo)

Texto para incluir na narrativa:

> "O desenvolvimento do {CORE TECNOLÓGICO — algoritmo, software, arquitetura} permanece integralmente executado pela equipe interna da Manacá, conforme detalhado nas Metas {LISTA}. A parceria com a {ICT X} limita-se à {DESCRIÇÃO DA PERIFERIA — ensaio/certificação/laudo/benchmark}, atividade cuja natureza exige {equipamento raro / certificação acreditada / isenção metodológica} disponível apenas em infraestrutura institucional especializada. As atividades da ICT estão vinculadas à rubrica 'Serviços de Terceiros' e totalizam {X}% do orçamento, dentro do limite estabelecido pelo edital. Não há transferência de código-fonte, direitos de PI ou arquétipos de desenho industrial para a ICT, preservando a capacidade absortiva da proponente e garantindo a retenção do conhecimento tecnológico ao final do projeto."

**Por quê esse parágrafo importa:**
- FINEP: o "Manual do Avaliador" exige demonstração explícita de capacidade absortiva.
- FAPESP: a regra de 1/3 ou 1/2 precisa de justificativa racional.
- EMBRAPII: há parceria por design, mas ainda assim o core da empresa deve ser reconhecível.

---

## Bloco 6 — Quando NÃO Incluir uma ICT

Nem todo edital pede ou se beneficia de ICT parceira. Avaliar com cuidado em editais:

- **Prêmios e aceleradoras:** normalmente desnecessário; pode inclusive diluir o story da empresa.
- **Editais de baixo orçamento:** não compensa o overhead documental.
- **Quando a Manacá tem todas as competências internas e o projeto não precisa de certificação externa.**
- **Quando a ICT parceira tem histórico fraco no tema específico** (pior que não ter — aciona dúvida).

---

## Bloco 7 — Rede de ICTs Potenciais (seed — expandir com o tempo)

| ICT | Localização | Área forte | Experiência prévia com Manacá | Status do relacionamento |
|---|---|---|---|---|
| UFES | Vitória/ES | Engenharia, tecnologias sociais | — | A prospectar |
| IFES | Vitória/ES | Engenharia aplicada, IoT | — | A prospectar |
| USP Poli | São Paulo/SP | Engenharia, automação, energia | Alumni: Alexandre Coleto | Alumni |
| PUC-SP | São Paulo/SP | Ciências Sociais, avaliação | Alumni: Rayssa Mendes | Alumni |
| Columbia University | Nova York/EUA | Educação internacional | Alumni: Ângelo Santos | Alumni |
| UTFPR | Curitiba/PR | Engenharia de Computação, IA | Alumni: Gabriel Candelaria | Alumni |
| {preencher} | {...} | {...} | {...} | {...} |

**Ação recomendada:** expandir essa tabela organicamente. Cada edital em que uma ICT parceira foi usada (ou cogitada), registrar aqui para reutilizar depois.

---

## Checklist

- [ ] Atividades da ICT são de periferia (não são o core)
- [ ] Rubrica correta (Serviços de Terceiros — não Equipe Executora)
- [ ] Respeita limite orçamentário da agência
- [ ] ACT anexado (ou minuta pré-acordada)
- [ ] Carta de Anuência Institucional anexada
- [ ] Carta de Anuência Individual anexada
- [ ] Lattes do pesquisador ICT atualizado
- [ ] Declaração de blindagem do core está na narrativa
- [ ] Justificativa técnica da escolha da ICT está clara (por que essa e não outra?)
