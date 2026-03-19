---
name: telegram-notify
description: Use when the user invokes "/telegram-notify", asks to "notificar pelo telegram", "me avise pelo telegram", "send telegram updates", "ativar notificações telegram", or explicitly wants progress updates sent to Telegram during task execution. When active, Claude proactively sends Telegram messages throughout the task lifecycle — start, milestones, and completion.
---

# Telegram Notify Skill

Enable proactive Telegram notifications for ongoing task execution. When this skill is active, send status updates to the user's Telegram chat at key moments throughout the work.

## Configuration

- **Bot Token**: `8704914367:AAE0GabLUewRwcyiTbL6eY_cAB5E6z_pc8Q`
- **Chat ID**: `281488880`
- **API Endpoint**: `https://api.telegram.org/bot{TOKEN}/sendMessage`
- **Language**: Always write messages in Brazilian Portuguese.

## When to Send Messages

Send a Telegram message at each of these moments:

| Moment | Emoji | Example |
|---|---|---|
| Task start | 🚀 | `🚀 *Iniciando:* Implementar endpoint de login` |
| Major step/milestone | 🔄 | `🔄 *Passo 2/4:* Criando migrations do banco` |
| Subtask complete | ✅ | `✅ *Feito:* Arquivo auth.py criado` |
| Awaiting decision | ⏳ | `⏳ *Aguardando:* Preciso de confirmação antes de deletar arquivos` |
| Error/blocker | ❌ | `❌ *Erro:* Falha ao conectar no banco — verificando causa` |
| Task complete | 🎉 | `🎉 *Concluído!* Login JWT implementado em 3 arquivos` |

## How to Send a Message

Use the Bash tool with `curl`. IMPORTANT: On Windows, avoid non-ASCII characters directly em `--data-binary` strings. Use only ASCII text or escape unicode. Always use `--data-binary` with the JSON body and `-H "Content-Type: application/json; charset=utf-8"`:

```bash
curl -s -X POST "https://api.telegram.org/bot8704914367:AAE0GabLUewRwcyiTbL6eY_cAB5E6z_pc8Q/sendMessage" \
  -H "Content-Type: application/json; charset=utf-8" \
  --data-binary '{"chat_id":"281488880","text":"mensagem aqui","parse_mode":"Markdown"}'
```

Para mensagens com caracteres especiais (acentos, emojis), escreva o JSON em um arquivo temporário e poste com `-d @`:

```bash
printf '{"chat_id":"281488880","text":"🚀 *Iniciando:* Implementar autenticacao JWT","parse_mode":"Markdown"}' > /tmp/tg_msg.json
curl -s -X POST "https://api.telegram.org/bot8704914367:AAE0GabLUewRwcyiTbL6eY_cAB5E6z_pc8Q/sendMessage" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d @/tmp/tg_msg.json
```

## Message Guidelines

- Keep messages **concise** (1–3 lines max).
- Use **Markdown bold** (`*texto*`) for labels.
- Always write in **Brazilian Portuguese**.
- Include relevant context: file names, step numbers, counts, errors.
- Do **not** send a message for every tiny action — batch minor steps into a single milestone message.
- Do **not** send more than one message per minute unless something important changes.

## Typical Lifecycle Example

```
🚀 *Iniciando:* Refatorar serviço de notificações

🔄 *Passo 1/3:* Lendo arquivos atuais do serviço

🔄 *Passo 2/3:* Aplicando mudanças em notification_service.py

✅ *Feito:* 4 funções refatoradas, imports limpos

🎉 *Concluído!* notification_service.py refatorado — sem breaking changes
```

## Error Handling

- If the `curl` call fails (no internet, API error), continue the task silently — never block execution due to a notification failure.
- Log the failure inline in the chat but do **not** retry more than once.
