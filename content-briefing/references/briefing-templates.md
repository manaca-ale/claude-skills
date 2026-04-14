# Briefing Templates by Format

## Formatting Rules (Google Docs output)

These rules apply when writing briefings to Google Docs via `batch_update_doc`:

```
FONT_FAMILY: "Arial" (default Google Docs sans-serif)
TITLE_SIZE: 14pt, bold
SECTION_HEADING_SIZE: 12pt, bold (e.g., "01. Briefing para a agência")
SUBSECTION_HEADING_SIZE: 11pt, bold (e.g., "Objetivo do conteúdo:")
BODY_TEXT_SIZE: 11pt, normal
TEXT_COLOR: #000000 (black)
HORIZONTAL_RULE: "____________________________________________________________________________________________________" (100× underscore)
PAGE_BREAK: Insert between each briefing
FIELD_NAMES: Bold (e.g., "Objetivo do conteúdo:", "Público-alvo:", "Mensagem central:")
FIELD_CONTENT: Normal weight, same line or next line depending on length
BULLET_LISTS: Use standard Google Docs unordered list for público-alvo, pilares, etc.
```

## Common Header (all formats)

```
Título: {tema}
Formato: {Reels|Carrossel|Post único}
Status: Em produção
{if Reels or video: "Vídeo: [orientações sobre gravação]"}
{if needs photos: "Fotos: [orientações sobre fotos necessárias]"}
__________________________________________________________________________________________________________________
```

## Common Section "01. Briefing para a agência" (all formats)

Every briefing MUST include these fields in this order:

### Required Fields (all formats):

1. **Objetivo do conteúdo** (2-5 paragraphs)
   - Use GET WHO TO BY framework as the strategic core
   - Explain the WHY behind this piece of content
   - Connect to Manacá's strategic positioning
   - Mention what the post should achieve (educate, generate leads, build authority, celebrate, etc.)
   - When content is institutional: explain the role within the profile strategy

2. **Público-alvo** (bulleted list)
   - Always specific to THIS content piece (not generic)
   - Draw from brand-context.md target audiences
   - Include primary AND secondary audiences when relevant

3. **Mensagem central** (1-2 paragraphs)
   - The ONE thesis or insight the audience must internalize
   - Ground in Manacá's real capabilities and data
   - Clear, specific, not generic

4. **Tom e linguagem** (short bulleted list)
   - Calibrated per the tone-matrix.md
   - Typically 4-6 descriptors
   - Always include "Linguagem clara e acessível" or equivalent

### Format-Specific Fields:

#### Reels-specific:
5. **Diretrizes técnicas**:
   - Formato: Reels
   - Duração sugerida: [15-60s depending on content density]
   - Pessoa em cena: [Rayssa / outro / ninguém]
   - Sugestões de edição: [cortes dinâmicos, legendas na tela, B-roll, música de fundo]
6. **Pilares que precisam aparecer** (when institutional content)
7. **Contexto estratégico** (when part of a series or launch campaign)

#### Carrossel-specific:
5. **Papel no perfil / Função dentro da estratégia** (1-2 sentences explaining where this fits)
6. **Diretrizes de linguagem**:
   - Pouco texto por card
   - Frases-chave fortes
   - Um conceito por card
   - Hierarquia visual clara

#### Post único-specific:
5. **Elementos essenciais no card**:
   - Frase de impacto (principal)
   - Data em destaque (if commemorative)
   - Logo da Manacá
   - Visual direction

## Section "02. ROTEIRO COMPLETO" Templates

### Reels Script Template

```
02. ROTEIRO COMPLETO DO REELS
Observação: [Pessoa] não precisa seguir palavra por palavra, mas manter a lógica, as mensagens e as palavras-chave.

1. Abertura – Gancho (0–7s)
"[Hook question or provocative statement that creates immediate connection]"

2. [Topic development] (7–{midpoint}s)
"[Core message development - what the audience needs to understand]"

3. [Evidence/Data/Method] ({midpoint}–{near_end}s)
"[Supporting arguments, real data, methodology reference]"

4. Fechamento + CTA ({near_end}–{end}s)
"[Impactful closing + clear call to action]"
[Visual: Logo da Manacá]
```

Duration guidelines:
- Short/simple topic: 30-45s (3-4 scenes)
- Medium complexity: 45-60s (4-6 scenes)
- Complex/educational: 60-90s (5-7 scenes)

### Carrossel Script Template

```
02. ROTEIRO COMPLETO DO CARROSSEL

CARD 1 — CAPA
Título principal: [Strong, attention-grabbing headline]
Subtítulo (opcional): [Complementary line that adds context]
[Visual: institucional, com identidade Manacá]

CARD 2 — CONTEXTO / ABERTURA
Texto: [Set up the problem or context - why this matters]

CARD 3 — [CONCEPT/PILLAR 1]
Título: [Concept name]
Texto: [2-4 sentences explaining this concept clearly]

CARD 4 — [CONCEPT/PILLAR 2]
Título: [Concept name]
Texto: [2-4 sentences]

[... CARD N — additional concepts as needed ...]

CARD {N+1} — PROPÓSITO / FECHAMENTO
Texto: [Inspirational closing that connects back to Manacá's mission]

CARD {N+2} — CTA
Texto principal: [Call to action question]
Complemento: [How to take action / contact info]
[Visual: Logo da Manacá]
```

Card count guidelines:
- Simple awareness: 5-7 cards
- Educational/deep: 7-9 cards
- Case study / retrospective: 7-10 cards

### Post Único Script Template

```
02. ROTEIRO COMPLETO DO CARD

Elementos essenciais no card:
• Frase de impacto (principal): [The single headline that carries the message]
• {if commemorative date: "Data: [date] | [name of the date]"}
• Logo da Manacá
• [Any additional visual elements: icons, images, brand elements]

Legenda sugerida: [If LEGENDA was provided in input, include it here with minor adjustments. If not provided, generate a complete caption following the brand voice.]
```

## Generation Guidelines

### When LEGENDA is provided:
- Use the caption as creative seed and strategic reference
- The briefing should ALIGN with the caption's tone and messaging
- The roteiro should support and extend the caption's narrative
- Do NOT contradict or diverge from the caption's direction

### When LEGENDA is empty:
- Generate the full creative direction from the TEMA alone
- Be more detailed in the briefing (extra context needed for the agency)
- Generate a suggested caption in the roteiro section
- Include more visual/editorial direction since the agency has less guidance

### Content editoria classification:
Use these categories to calibrate tone and depth:

| Editoria | Signals in TEMA | Tone modulation |
|----------|-----------------|-----------------|
| **Institucional** | "O que é", "Como faz", "Conheça", post fixado | More strategic, foundational, brand-building |
| **Educativo/Thought Leadership** | Concepts, methodologies, "por que", "como" | Didactic, accessible, data-grounded |
| **Engajamento/Celebração** | Dates, awards, partnerships, retrospective | Inspiring, proud, community-building |
| **Produto (Flora)** | "Flora", platform, dashboard, measurement | Educational-commercial, problem-solution |
| **Bastidores/Cultura** | Team, events, behind-the-scenes | Warm, authentic, human |
