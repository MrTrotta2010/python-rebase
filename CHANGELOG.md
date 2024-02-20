# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

Este formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
e este projeto adere ao [Versionamento Semântico](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2024-02-20

### Alterado
- A partir deste update, **qualquer usuário que quiser acessar o ReBase precisa ter um token de autenticação cadastrado no sistema**. Para receber um token, o usuário deve entrar em contato com o time de desenvolvimento através dos emails `mrtrotta2010@gmail.com` ou `diegocolombodias@gmail.com` e enviar o endereço de email que deseja cadastrar;
- O módulo `rebase_client` foi transformado na classe `ReBaseClient`. A classe ainda desempenha o mesmo papel, porém agora é necessário inicializá-la passando o email e o token cadastrados do usuário;
- No cabeçalho das requisições agora são enviados o email cadastrado e o token do usuário nos headers **"rebase-user-email"** e **"rebase-user-token"**.

## [0.2.3] - 2023-12-22

### Corrigido
- Erro em Movement.__force_registers que ignorava todos os registros após o primeiro.

### Alterado
- Ao criar movimento sem a propriedade 'articulations', ela será atribuida automaticamente a partir das articulações do primero registro, ao invés de lançar um `MismatchedArticulationsError`.

## [0.2.2] - 2023-12-21

### Corrigido
- Validação do objeto `app` para os Movimentos. Agora, ao criar um Movimento, são aceitos tanto os atributos separados `appCode` e `appData` quanto o objeto `'app': { 'code': str, 'data': any }`.

## [0.2.1] - 2023-12-18

### Corrigido
- Link do changelog na página do pacote no PyPi.

## [0.2.0] - 2023-12-18

### Adicionado
- Atributo `movement_ids` em `session`, contendo os IDs dos seus Movimentos. Esse campo é retornado nas requisições `fetch_sessions` e `find_session` quando o parâmetro `deep` está ausente ou tem o valor `False`.
- Indicador da versão atual no topo do arquivo `README.md`

## [0.1.3] - 2023-12-01

### Adicionado
- Arquivo de changelog;
- Link para o changelog na página do PyPi.

## [0.1.2] - 2023-12-01

### Alterado
- Renomeia o servidor de ReBase REST Server, ou RRS, para apenas **ReBaseRS**.
