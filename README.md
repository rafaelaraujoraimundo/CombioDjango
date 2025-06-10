# Projeto Suporte

Este projeto Django tem como objetivo fornecer funcionalidades relacionadas ao suporte de usuários, incluindo desligamentos, substituições e gerenciamento de acessos ao Fluig.

Inclui integração com diversos módulos da plataforma ComBio, ferramentas de administração, inventário, chatbot, e APIs internas.

## 🚀 Execução do Projeto

### Requisitos

- Python 3.11+
- Docker + docker-compose
- PostgreSQL

### Instalação

```bash
pip install -r requirements.txt
```

### Docker

```bash
docker-compose up --build
```

## 📂 Estrutura de Pastas
- `administration/`
- `api_v1/`
- `chatbot/`
- `cofre/`
- `combio/`
- `comunicacao/`
- `contrib/`
- `dashboard/`
- `inventario/`
- `menu/`
- `novosProjetos/`
- `routers/`
- `suporte/`
- `utils/`

## 📚 Descrição dos Módulos

### `administration`
- **Total de funções:** 36
- **Total de classes:** 25
- **Exemplos de funções:** `delete_user`, `decrypt_password`, `encrypt_password`
- **Exemplos de classes:** `Recurso`, `Documento`, `Requisicao`

### `api_v1`
- **Total de funções:** 7
- **Total de classes:** 25
- **Exemplos de funções:** `get_FluigServer`, `get_consultas_api`, `get_consultas_flask`
- **Exemplos de classes:** `FiltroQuerySet`, `UsuarioRH`, `FluxoPE6`

### `chatbot`
- **Total de funções:** 17
- **Total de classes:** 10
- **Exemplos de funções:** `should_send_initial_message`, `formatar_titulos_em_blocos`, `formatar_titulos_pagos_em_blocos`
- **Exemplos de classes:** `MockAPI`, `ChatMessage`, `RespostaWhats`

### `cofre`
- **Total de funções:** 4
- **Total de classes:** 4
- **Exemplos de funções:** `pesquisa_item`, `pesquisa_movimentacao`, `form_valid`
- **Exemplos de classes:** `ItemCofre`, `Movimentacao`, `HistoricoItem`

### `combio`
- **Total de funções:** 5
- **Total de classes:** 6
- **Exemplos de funções:** `tipo_unidade_display`, `get_queryset`, `tem_processo_aberto`
- **Exemplos de classes:** `Setor`, `Empresa`, `Movimentacao`

### `comunicacao`
- **Total de funções:** 3
- **Total de classes:** 8
- **Exemplos de funções:** `noticia_aleatoria`, `pesquisa_satisfacao`, `abrir_feedback`
- **Exemplos de classes:** `Comunicado`, `Noticia`, `Feedback`

### `contrib`
- **Total de funções:** 0
- **Total de classes:** 1
- **Exemplos de classes:** `PDFTemplateResponse`

### `dashboard`
- **Total de funções:** 5
- **Total de classes:** 4
- **Exemplos de funções:** `get_setor`, `get_queryset`, `get_filtros`
- **Exemplos de classes:** `Painel`, `Filtro`, `Indicador`

### `inventario`
- **Total de funções:** 24
- **Total de classes:** 21
- **Exemplos de funções:** `exportar_csv`, `verificar_ativos`, `get_patrimonios`
- **Exemplos de classes:** `Ativo`, `NotaFiscal`, `Transferencia`

### `menu`
- **Total de funções:** 5
- **Total de classes:** 13
- **Exemplos de funções:** `carregar_menu`, `montar_menu`, `get_menu_usuario`
- **Exemplos de classes:** `MenuItem`, `Permissao`, `Modulo`

### `novosProjetos`
- **Total de funções:** 6
- **Total de classes:** 9
- **Exemplos de funções:** `novo_projeto`, `finalizar_projeto`, `desativar_projeto`
- **Exemplos de classes:** `Projeto`, `Demanda`, `Tarefa`

### `routers`
- **Total de funções:** 0
- **Total de classes:** 0

### `suporte`
- **Total de funções:** 9
- **Total de classes:** 15
- **Exemplos de funções:** `update_usuario_fluig`, `form_valid`, `verificar_bloqueios_pendentes`
- **Exemplos de classes:** `UsuarioDesligamento`, `UsuarioFluig`, `Substituicao`

### `utils`
- **Total de funções:** 8
- **Total de classes:** 9
- **Exemplos de funções:** `pasta_upload_ativo_valores`, `data_valida`, `cnpj_valido`
- **Exemplos de classes:** `CustomPaginator`, `DataFormatter`, `FluigAPI`
