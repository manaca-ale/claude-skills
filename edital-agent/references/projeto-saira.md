---
last_verified: 2026-04-13
next_review: 2026-07-13
stale_fields:
  - registro_software ([PREENCHER] pendente)
---

# Projeto SAÍRA — Sistema de Alerta Inteligente para Resíduos e Autuações

## Resumo

O SAÍRA é uma solução tecnológica híbrida para monitoramento, fiscalização, autuação e gestão inteligente do descarte irregular de resíduos sólidos urbanos. Integra software, inteligência artificial, visão computacional e dados georreferenciados para apoiar o poder público.

## Status Atual

| Campo | Valor |
|-------|-------|
| TRL | ~6 (MVP funcional com testes em ambiente controlado) |
| Cliente principal | Prefeitura do Recife (via CPSI) |
| Contrato | CPSI firmado via inovação aberta, perspectiva de até R$ 8 milhões |
| Tipo de cliente | B2G (Business to Government) |

### CPSI — Contrato Público de Solução Inovadora

| Campo | Valor |
|-------|-------|
| Marco legal | Lei Complementar nº 182/2021 (Marco Legal das Startups) |
| Parceiros | Prefeitura do Recife + Manacá Tecnologias Sociais |
| Modelo | Inovação aberta — chamada pública para startups |
| Piloto | 10 pontos críticos, 10 câmeras, 10 bairros |
| Bairros do piloto | Imbiribeira, Brasília Teimosa, Santo Amaro, Prado, Porto da Madeira, Arruda, Torrões, Várzea, Jiquiá, Campo Grande |
| Fase 2 (previsão) | Escala para ~150 pontos cobertos |
| Perspectiva de contrato | Até R$ 8 milhões |

O CPSI permite ao poder público contratar startups para desenvolver, testar e validar soluções inovadoras ainda inexistentes no mercado, com segurança jurídica e foco em resultados. Rompe com a lógica tradicional de compras públicas, aproximando o Estado da experimentação e da inovação.

### Status de Desenvolvimento (jan/2026)

| Entrega | Status |
|---------|--------|
| Mockup alta fidelidade (Figma) | Validado |
| Arquitetura de software | Desenhada e documentada |
| Infraestrutura cloud (AWS) | Configurada |
| Dataset v1.0 (10K+ imagens) | Preparado e categorizado |
| Próxima fase | Desenvolvimento do backend |

> Nota: Detalhes técnicos de arquitetura (AWS, YOLO, S3) ficam nos repos GitHub do projeto.

## Arquitetura da Solução

### 3 Camadas Funcionais
1. **Monitoramento e Detecção** — Câmeras com IA, drones, sensores IoT, app de denúncia cidadã
2. **Processamento e Análise** — Motor de IA (YOLO), georreferenciamento, análise de riscos, motor de match socioambiental
3. **Ação e Destinação** — Dashboard de gestão, fiscalização automatizada, logística de limpeza, relatórios de impacto

### Módulos do MVP
1. **IA para Visão Computacional** — Detecção de resíduos em imagens, classificação de tipo/volumetria, registro de reincidência
2. **App Web Mobile** — Foto obrigatória + localização automática + tipo de resíduo + envio (React Native)
3. **Dashboard de Gestão Pública** — Mapa interativo, histórico de ocorrências, alertas, exportação CSV
4. **Integração com Sistemas da Prefeitura** — API/CSV para CTTU, Emlurb, Defesa Civil

## Diferenciais
- **Modular:** implementação por partes (começar com monitoramento, depois fiscalização e Reciclo Social)
- **Escalável:** funciona em bairros, cidades inteiras ou regiões metropolitanas
- **Integrável:** conecta com sistemas existentes da Prefeitura
- **Inteligência Social:** transforma resíduos de problema urbano em oportunidade social e econômica

## Editais Vencidos

### Eita Recife!
- **Programa:** Eita! Recife
- **Escopo:** MVP de monitoramento inteligente de resíduos
- **Foco:** 5-10 pontos críticos de Recife (1.700+ pontos de descarte irregular)
- **Prazo do MVP:** 3 meses
- **Status:** Vencedor

### Empreendedoras Tech
- **Programa:** Empreendedoras Tech (provavelmente aceleração)
- **Escopo:** Mesmo SAÍRA, foco no potencial de expansão
- **Status:** Vencedor

## Desafios Tecnológicos Principais
1. Integração de múltiplas fontes de dados urbanos em plataforma única
2. Detecção robusta em escala urbana (variações de iluminação, clima, tipos de resíduo)
3. Identificação de infratores sem uso de dados biométricos sensíveis (foco em veículos e comportamento)
4. Baixo índice de falsos positivos em ambiente real

## Propriedade Intelectual

| Campo | Valor |
|-------|-------|
| Código-fonte | Proprietário da Manacá |
| Modelos de IA | Treinados pela equipe Manacá |
| Registro de software | [PREENCHER] |

## Impacto Social e Ambiental
- Redução de pontos de descarte irregular
- CO₂ evitado pela gestão inteligente
- Volume de resíduos reaproveitados (economia circular via Reciclo Social)
- Geração de renda para comunidades
- Melhoria da saúde pública (redução de doenças relacionadas a resíduos)

## ODS Relacionados
- ODS 11: Cidades e Comunidades Sustentáveis
- ODS 12: Consumo e Produção Responsáveis
- ODS 13: Ação contra a Mudança Global do Clima
- ODS 3: Saúde e Bem-Estar
