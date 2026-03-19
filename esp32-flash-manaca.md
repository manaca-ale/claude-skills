---
name: esp32-flash-manaca
description: Gravar firmware do projeto SAIRA na placa ESP32 conectada por porta COM, atualizando automaticamente o .env antes do flash. Use quando o usuario pedir para gravar/flashar firmware na ESP32, escrever um novo ID de dispositivo no formato esp32_xxx, ajustar WIFI_SSID para Manaca_ID, ou executar upload PlatformIO para a placa.
---

# ESP32 Flash Manaca

## Workflow

1. Perguntar o ID antes de qualquer alteracao:
   `Qual ID devo gravar? Use o formato esp32_xxx.`
2. Validar que o ID segue `^esp32[-_][a-zA-Z0-9_-]+$`.
3. Executar o script deste skill para atualizar `WIFI_SSID` e `DEVICE_ID` no `.env`:
   `python C:\Users\aleco\.codex\skills\esp32-flash-manaca\scripts\flash_manaca.py --device-id <ID> --repo-root <repo>`
4. Se o usuario informar uma porta COM especifica, incluir `--port COMx`.
5. Reportar o resultado com:
   - caminho do `.env` atualizado
   - valor final de `WIFI_SSID` (`Manaca_<ID>`)
   - porta usada
   - status final do upload

## Commands

- Atualizar `.env` e gravar automaticamente:
  `python C:\Users\aleco\.codex\skills\esp32-flash-manaca\scripts\flash_manaca.py --device-id esp32_002 --repo-root C:\saira`
- Atualizar `.env` e forcar porta:
  `python C:\Users\aleco\.codex\skills\esp32-flash-manaca\scripts\flash_manaca.py --device-id esp32_002 --repo-root C:\saira --port COM20`
- Somente preflight (sem gravar):
  `python C:\Users\aleco\.codex\skills\esp32-flash-manaca\scripts\flash_manaca.py --device-id esp32_002 --repo-root C:\saira --dry-run`

## Defaults

- Firmware env: `ipcam-relay-esp32s3-devkitc-1-n16r8`
- Arquivo de configuracao: `<repo-root>\firmware\espcam-saira\.env`
- SSID final: `Manaca_<ID>`

## Safety

- Nunca gravar com ID fora do formato esperado.
- Se nao detectar porta USB unica, pedir porta COM explicitamente.
- Se o upload falhar, reportar o erro bruto do `platformio` e nao assumir sucesso.
