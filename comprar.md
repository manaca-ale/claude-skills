---
name: comprar
description: "Automatiza compras no site Carone a partir de lista.xlsx usando Playwright com analise visual inteligente. Use quando o usuario pedir para fazer compras, rodar o robo de mercado, ou adicionar produtos ao carrinho do Carone."
---

# Robo de Compras Carone — Skill Inteligente

Automatiza compras no site carone.com.br lendo uma planilha de produtos e usando o Playwright CLI para navegar, buscar, analisar visualmente os resultados e adicionar ao carrinho.

**Voce e o cerebro do robo.** Em vez de usar seletores CSS frageis ou matching de tokens, voce VE a tela via snapshots e toma decisoes inteligentes sobre qual produto escolher.

## Contexto Fixo

| Parametro | Valor |
| --- | --- |
| Diretorio do projeto | `c:/Users/aleco/RobomercadoCarone` |
| Planilha de entrada | `c:/Users/aleco/RobomercadoCarone/lista.xlsx` |
| Relatorio de saida | `c:/Users/aleco/RobomercadoCarone/relatorio_carrinho.xlsx` |
| Historico de compras | `c:/Users/aleco/RobomercadoCarone/Basededados.xlsx` |
| Site alvo | `https://www.carone.com.br/` |
| Perfil Chrome | `c:/Users/aleco/RobomercadoCarone/chrome_debug_profile` |
| Porta debug Chrome | `9222` |

## Pre-requisitos (verificar antes de comecar)

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"
command -v npx >/dev/null 2>&1 && echo "npx OK" || echo "ERRO: npx nao encontrado"
test -f "$PWCLI" && echo "Playwright CLI OK" || echo "ERRO: Playwright CLI nao encontrado"
test -f "c:/Users/aleco/RobomercadoCarone/lista.xlsx" && echo "lista.xlsx OK" || echo "ERRO: lista.xlsx nao encontrado"
```

Se algum pre-requisito falhar, oriente o usuario e PARE.

## Estrutura de lista.xlsx

| Coluna | Tipo | Descricao |
| --- | --- | --- |
| Produto | string | Nome do produto a buscar |
| Quantidade | float→int | Unidades desejadas (minimo 1) |
| Tipo de busca | string | `"Marca"` = incluir marca na busca. `"Preco"` = ordenar por menor preco |
| Marca | string | Nome da marca (usado se Tipo de busca contiver "marca") |
| Coluna 5 (nome varia) | bool | `TRUE` = comprar, `FALSE/0/N/NAO` = pular item |

Logica do termo de busca:
- Se "marca" em `Tipo de busca` E `Marca` preenchida → buscar `"{Produto} {Marca}"`
- Senao → buscar `"{Produto}"`

---

## Workflow

### Fase 1: Ler a planilha

Use Python para ler `lista.xlsx` e extrair os dados:

```bash
cd "c:/Users/aleco/RobomercadoCarone" && python -c "
import pandas as pd
df = pd.read_excel('lista.xlsx')
total = len(df)
# Coluna 5 (flag de compra) - pode ter nomes variados
flag_col = df.columns[4] if len(df.columns) > 4 else None
if flag_col:
    skip_vals = {'false','falso','0','nao','n','no'}
    comprar = df[~df[flag_col].astype(str).str.strip().str.lower().isin(skip_vals)]
else:
    comprar = df
pulados = total - len(comprar)
print(f'TOTAL: {total} produtos | COMPRAR: {len(comprar)} | PULAR: {pulados}')
print('---LISTA---')
for i, row in comprar.iterrows():
    produto = str(row.get('Produto','')).strip()
    qtd = int(round(float(row['Quantidade']))) if pd.notna(row.get('Quantidade')) else 1
    qtd = max(qtd, 1)
    tipo = str(row.get('Tipo de busca','')).lower()
    marca = str(row.get('Marca','')).strip()
    if marca == 'nan': marca = ''
    termo = f'{produto} {marca}'.strip() if 'marca' in tipo and marca else produto
    preco = 'preco' in tipo
    print(f'{i}|{termo}|{qtd}|{\"PRECO\" if preco else \"NORMAL\"}')
"
```

Apresente o resumo ao usuario: quantos produtos serao comprados, quantos pulados.
Pergunte se quer prosseguir.

### Fase 2: Conectar ao browser

**Passo 1** — Verificar se Chrome ja esta rodando com debug port:

```bash
curl -s http://localhost:9222/json/version 2>/dev/null && echo "Chrome CDP ativo" || echo "Chrome NAO conectado"
```

**Passo 2** — Se Chrome NAO esta conectado, iniciar:

```bash
"/c/Program Files/Google/Chrome/Application/chrome.exe" \
  --remote-debugging-port=9222 \
  --user-data-dir="c:/Users/aleco/RobomercadoCarone/chrome_debug_profile" &
sleep 3
```

**Passo 3** — Conectar Playwright e abrir o site:

```bash
"$PWCLI" open https://www.carone.com.br/ --headed
```

**Passo 4** — Snapshot e verificar se o usuario esta logado:

```bash
"$PWCLI" snapshot
```

Analise o snapshot. Se voce ver indicios de que o usuario NAO esta logado (botao "Entrar", "Login", ausencia de nome do usuario), pergunte:

> "Voce precisa fazer login no site. Por favor, logue manualmente na janela do Chrome que foi aberta e me avise quando terminar."

Se ja estiver logado, prossiga.

### Fase 3: Loop de compras

Para CADA produto da lista, execute este ciclo:

#### 3a. Informar progresso

Imprima no terminal: `[X/N] Buscando: "{termo}" (qtd: {quantidade})`

#### 3b. Navegar para pagina inicial

```bash
"$PWCLI" navigate https://www.carone.com.br/
"$PWCLI" snapshot
```

#### 3c. Buscar o produto

No snapshot, identifique o campo de busca (geralmente um input de texto com placeholder tipo "O que voce procura?" ou similar).

```bash
"$PWCLI" fill eX "{termo_busca}"
"$PWCLI" press Enter
```

Aguarde carregamento:

```bash
sleep 3
"$PWCLI" snapshot
```

#### 3d. Analisar resultados (PONTO CRITICO)

**Este e o momento em que voce usa sua inteligencia.** Analise o snapshot dos resultados e:

1. **Identifique os produtos listados** — leia nomes, marcas, tamanhos, precos
2. **Escolha o melhor match** seguindo esta prioridade:
   - Correspondencia exata de marca (se especificada)
   - Nome do produto mais proximo ao buscado
   - Se tipo = "Preco": preferir o mais barato entre os que correspondem
3. **Se nenhum resultado** (pagina mostra "nenhum produto encontrado" ou similar):
   - Se a busca incluia marca, tente novamente so com o nome do produto
   - Se ainda nao encontrar, registre como "Nao encontrado" e prossiga para o proximo
4. **Se resultado ambiguo** (produtos muito diferentes do buscado):
   - Pergunte ao usuario qual escolher antes de clicar

#### 3e. Adicionar ao carrinho

**Estrategia A — Compra direta no card (preferivel):**

Se o card do produto tem botao "Comprar" ou "Adicionar" visivel no snapshot:

```bash
"$PWCLI" click eY    # botao Comprar do produto escolhido
sleep 1
"$PWCLI" snapshot    # confirmar
```

**Estrategia B — Via pagina do produto (PDP):**

Se nao ha botao de compra direto, clique no nome/imagem do produto para ir a pagina de detalhes:

```bash
"$PWCLI" click eY    # link do produto
sleep 2
"$PWCLI" snapshot    # pagina do produto
```

Na pagina do produto, localize o botao de adicionar ao carrinho.

#### 3f. Ajustar quantidade

Se `quantidade > 1`, localize o botao "+" no snapshot e clique `quantidade - 1` vezes:

```bash
"$PWCLI" click eZ    # botao "+"
sleep 0.3
# repetir para cada unidade adicional
```

Depois clique em "Comprar" / "Adicionar ao carrinho" se ainda nao clicou.

#### 3g. Confirmar adicao

```bash
"$PWCLI" snapshot
```

Verifique no snapshot se o produto foi adicionado (mensagem de sucesso, mini-carrinho atualizado, etc).

#### 3h. Fechar interferencias

Se modais, popups de cookies, chat widgets ou overlays aparecerem em qualquer snapshot, feche-os antes de continuar (clique no X, "Fechar", "Aceitar", ou pressione Escape).

#### 3i. Registrar resultado

Mantenha uma lista interna com o resultado de cada produto:
- `termo_buscado`: o que foi buscado
- `nome_no_site`: nome real do produto adicionado
- `quantidade`: unidades
- `status`: "Adicionado ao carrinho" | "Nao encontrado no site" | "Erro ao processar" | "Pulado (desmarcado)"
- `data_hora`: timestamp

### Fase 4: Gerar relatorio

Apos processar todos os produtos, gere o relatorio Excel:

```bash
cd "c:/Users/aleco/RobomercadoCarone" && python -c "
import pandas as pd
from datetime import datetime

# Substitua os dados abaixo pelos resultados reais coletados
dados = [
    # {'Termo Buscado': '...', 'Nome no Site': '...', 'Quantidade': 1, 'Status': '...', 'Data/Hora': '...'},
]

df = pd.DataFrame(dados)
colunas = ['Termo Buscado', 'Nome no Site', 'Quantidade', 'Status', 'Data/Hora']
df = df[[c for c in colunas if c in df.columns]]
df.to_excel('relatorio_carrinho.xlsx', index=False)
print(f'Relatorio salvo com {len(df)} itens.')
"
```

### Fase 5: Abrir carrinho e resumo

Navegue para o carrinho:

```bash
"$PWCLI" navigate https://www.carone.com.br/checkout/cart
"$PWCLI" snapshot
```

Apresente o resumo final ao usuario:

> **Compras finalizadas!**
> - X produtos adicionados ao carrinho
> - Y produtos nao encontrados
> - Z produtos pulados
> - Relatorio salvo em `relatorio_carrinho.xlsx`
> - O carrinho esta aberto no navegador para conferencia.

---

## Diretrizes de Decisao

### Escolha de produto
- **Marca e rei**: se o usuario especificou marca, o produto DEVE ser daquela marca, mesmo que outro seja mais barato
- **Tamanho importa**: "leite 1L" nao e a mesma coisa que "leite 200ml" — preste atencao
- **Erros de digitacao**: o usuario pode escrever "mateiga" querendo dizer "manteiga" — voce entende, o matching de tokens nao
- **Na duvida, pergunte**: se dois produtos parecem igualmente validos, pergunte ao usuario

### Tratamento de erros
- **Snapshot falhou**: tente novamente com `"$PWCLI" snapshot`
- **Pagina nao carregou**: aguarde mais (`sleep 3`) e tente re-snapshot
- **Botao nao encontrado**: tente scroll (`"$PWCLI" scroll down`) e re-snapshot
- **Modal bloqueando**: feche (Escape ou clique no X) e re-snapshot
- **Erro critico**: tire screenshot (`"$PWCLI" screenshot`), registre o erro, pergunte ao usuario se deve continuar

### Performance
- Nao precisa ser rapido — precisa ser correto
- Faca snapshot sempre que a pagina mudar
- Prefira certeza sobre velocidade
