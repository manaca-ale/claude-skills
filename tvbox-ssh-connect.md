---
name: tvbox-ssh-connect
description: Conectar e operar a TV Box TanixW2 via SSH para diagnostico, manutencao e execucao de comandos remotos. Use quando o usuario pedir para acessar a TV Box, entrar no servidor remoto da TV Box, validar conectividade SSH, coletar informacoes do sistema remoto, ou executar comandos no host TanixW2.
---

# TV Box SSH Connect

## Overview

Usar este skill para executar conexao SSH na TV Box configurada como `TanixW2` no `C:\Users\aleco\.ssh\config`.
Priorizar verificacao de conectividade e depois executar comandos remotos solicitados.

## Workflow

1. Validar que o alias SSH existe no arquivo `C:\Users\aleco\.ssh\config` com `Host TanixW2`.
2. Testar conectividade com comando nao interativo:
   `ssh -o ConnectTimeout=8 -o BatchMode=yes TanixW2 "echo TVBOX_OK && uname -a"`
3. Executar comando remoto solicitado:
   `ssh TanixW2 "<comando>"`
4. Abrir sessao interativa somente quando o usuario pedir explicitamente:
   `ssh TanixW2`

## Fallbacks

- Se o alias nao existir, usar `ssh root@192.168.0.10`.
- Se houver erro de autenticacao ou host key, reportar o erro exato e pedir orientacao antes de alterar credenciais/chaves.
- Se a rede estiver indisponivel, informar que nao foi possivel conectar e incluir a saida do erro.

## Safety

- Nao executar comandos destrutivos remotos sem pedido explicito do usuario.
- Em acoes de risco (remocao, reset, alteracao de configuracao), confirmar antes de executar.
